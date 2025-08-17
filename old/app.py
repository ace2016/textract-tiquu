import streamlit as st
import tempfile, os, re, zipfile, time
from io import BytesIO, StringIO
from pdfminer.high_level import extract_text
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import spacy
from sentence_transformers import SentenceTransformer, util
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

@st.cache_resource
def load_models(model_name):
    return spacy.load("en_core_web_sm"), SentenceTransformer(model_name)

st.set_page_config(page_title="Paragraph Coherence Analyzer", layout="wide")
st.title("📄 Research Paragraph Splitter + Coherence Scoring")

model_choice = st.sidebar.selectbox("Embedding Model", ["MPNet (accurate)", "MiniLM (fast)"])
model_name = "sentence-transformers/all-mpnet-base-v2" if "MPNet" in model_choice else "all-MiniLM-L6-v2"
nlp, embedder = load_models(model_name)

TRANSITIONS = ["however", "therefore", "in conclusion", "additionally", "next", "this study"]

uploaded_file = st.file_uploader("Upload a research PDF (scanned or digital)", type=["pdf"])

def is_image_pdf(path):
    try:
        reader = PdfReader(path)
        for page in reader.pages:
            if "/Font" in page.get("/Resources", {}):
                return False
    except:
        return True
    return True

def extract_text_safely(path):
    if is_image_pdf(path):
        st.warning("📸 Image-based PDF detected. Running OCR...")
        images = convert_from_path(path)
        return "\n".join(pytesseract.image_to_string(img) for img in images)
    else:
        st.info("📝 Text-based PDF detected. Extracting text...")
        return extract_text(path)

def clean_text(text):
    patterns = [
        r"(?i)OPEN ACCESS", r"www\.\S+", r"doi:\S+", r"ISSN \d+", r"E[-]?Mail:.*?\n",
        r"Tel\.:.*?\n", r"Fax\.:.*?\n", r"Received:.*?\n", r"Accepted:.*?\n", r"Published:.*?\n",
        r"\bCorrespondence\b.*", r"\* Author.*?\n", r"^\s*\d{1,2}\s*$", r"\n{2,}"
    ]
    for pattern in patterns:
        text = re.sub(pattern, "", text)
    return text.strip()

SECTION_HEADERS = [
    "abstract", "introduction", "background", "literature review", "related work",
    "method", "methodology", "approach", "results", "experiments",
    "discussion", "conclusion", "references", "acknowledgements"
]

def detect_sections(text):
    pattern = r"\n\s*(?:" + "|".join(SECTION_HEADERS) + r")\s*\n"
    matches = list(re.finditer(pattern, text, flags=re.IGNORECASE))
    if not matches:
        return [("Full Text", text)]
    sections = []
    for i in range(len(matches)):
        start = matches[i].end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        title = matches[i].group(0).strip()
        content = text[start:end].strip()
        sections.append((title, content))
    return sections

def coherence_score(paragraph):
    sents = [s.strip() for s in paragraph.split(".") if len(s.strip().split()) > 3]
    if len(sents) < 2:
        return 1.0, 0, 0
    embeddings = embedder.encode(sents, convert_to_tensor=True)
    sim_matrix = util.cos_sim(embeddings, embeddings)
    adj_scores = [sim_matrix[i][i+1].item() for i in range(len(sents)-1)]
    incoherent = sum(1 for s in adj_scores if s < 0.65)
    return sum(adj_scores) / len(adj_scores), len(adj_scores), incoherent

def runtime_warning(runtime, page_count):
    if page_count <= 8 and runtime > 3:
        return True
    elif page_count <= 15 and runtime > 7:
        return True
    elif page_count <= 32 and runtime > 12:
        return True
    elif page_count <= 100 and runtime > 30:
        return True
    return False

if uploaded_file:
    timers = {}
    timers["start"] = time.time()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    timers["extraction_start"] = time.time()
    raw_text = extract_text_safely(pdf_path)
    timers["extraction_end"] = time.time()

    os.remove(pdf_path)
    page_count = raw_text.count("\f")
    cleaned_text = clean_text(raw_text)
    sections = detect_sections(cleaned_text)

    timers["split_start"] = time.time()

    min_words, max_words = 180, 280
    all_paragraphs = []

    for title, content in sections:
        doc = nlp(content)
        sents = [s.text.strip() for s in doc.sents if s.text.strip()]
        current_para, word_count = [], 0
        for sent in sents:
            current_para.append(sent)
            word_count += len(sent.split())
            should_split = word_count >= max_words or (
                word_count >= min_words and sent.endswith(".")
            )
            if should_split:
                paragraph = " ".join(current_para)
                score, pairs, incoherent = coherence_score(paragraph)
                all_paragraphs.append({
                    "Paragraph #": len(all_paragraphs) + 1,
                    "Words": len(paragraph.split()),
                    "Coherence Score": round(score, 3),
                    "Sentence Pairs": pairs,
                    "Incoherent Pairs": incoherent,
                    "Flag": "⚠️" if score < 0.85 else "✅",
                    "Length Flag": "⚠️ Too Short" if len(paragraph.split()) < 100 else "✅",
                    "Paragraph Text": paragraph
                })
                current_para, word_count = [], 0

        if current_para:
            paragraph = " ".join(current_para)
            score, pairs, incoherent = coherence_score(paragraph)
            all_paragraphs.append({
                "Paragraph #": len(all_paragraphs) + 1,
                "Words": len(paragraph.split()),
                "Coherence Score": round(score, 3),
                "Sentence Pairs": pairs,
                "Incoherent Pairs": incoherent,
                "Flag": "⚠️" if score < 0.85 else "✅",
                "Length Flag": "⚠️ Too Short" if len(paragraph.split()) < 100 else "✅",
                "Paragraph Text": paragraph
            })

    timers["end"] = time.time()
    runtime = round(timers["end"] - timers["start"], 2)

    if all_paragraphs:
        df = pd.DataFrame(all_paragraphs)
        df_sorted = df.sort_values(by="Coherence Score", ascending=False).reset_index(drop=True)

        st.subheader(f"📊 Paragraph Analysis (Total: {len(df_sorted)} | Runtime: {runtime}s)")
        st.dataframe(df_sorted)

        if runtime_warning(runtime, page_count):
            st.error(f"⚠️ Runtime exceeded brief target for {page_count} page(s)!")

        st.info(f"""
⏱️ Runtime Breakdown:
- Text Extraction: {timers["extraction_end"] - timers["extraction_start"]:.2f}s
- Splitting + Scoring: {timers["end"] - timers["split_start"]:.2f}s
- Total: {runtime:.2f}s
""")

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df_sorted["Coherence Score"], marker="o", color='blue')
        ax.axhline(0.85, color="red", linestyle="--", label="Target 0.85")
        ax.set_title("Paragraph Coherence Scores")
        ax.set_xlabel("Paragraph Index")
        ax.set_ylabel("Score")
        ax.grid(True)
        ax.legend()

        img_buf = BytesIO()
        fig.savefig(img_buf, format="png")
        img_buf.seek(0)

        txt = StringIO()
        txt.write("=== Paragraph Report ===\n")
        txt.write(f"Runtime: {runtime} seconds\nTotal Paragraphs: {len(df_sorted)}\n")
        txt.write(f"Average Score: {round(df_sorted['Coherence Score'].mean(), 3)}\n\n")

        for _, row in df_sorted.iterrows():
            txt.write("\n" + "="*60 + "\n")
            txt.write(f"Paragraph #: {row['Paragraph #']} | Score: {row['Coherence Score']} | Flag: {row['Flag']}\n")
            txt.write(f"Words: {row['Words']}, Sentence Pairs: {row['Sentence Pairs']}, Incoherent: {row['Incoherent Pairs']}\n")
            txt.write(row["Paragraph Text"] + "\n")

        csv_buf = StringIO()
        df_sorted.to_csv(csv_buf, index=False)
        zip_buf = BytesIO()
        with zipfile.ZipFile(zip_buf, "a", zipfile.ZIP_DEFLATED) as z:
            z.writestr("paragraphs.txt", txt.getvalue())
            z.writestr("paragraphs.csv", csv_buf.getvalue())
            z.writestr("coherence_plot.png", img_buf.getvalue())
        zip_buf.seek(0)

        st.download_button("Download ZIP (TXT + CSV + Plot)", zip_buf, "results.zip", mime="application/zip")
        st.download_button("Download TXT", txt.getvalue(), "paragraphs.txt", mime="text/plain")
        st.download_button("Download CSV", csv_buf.getvalue(), "paragraphs.csv", mime="text/csv")
        st.download_button("Download Plot", img_buf, "coherence_plot.png", mime="image/png")
    else:
        st.warning("❌ No paragraphs found.")
