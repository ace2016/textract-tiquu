import json
import re

import pdfplumber
import os
from pathlib import Path


# Function to clean the text
def cleanse_text(text):
    unwanted_sections = ["references"]
    for section in unwanted_sections:
        pattern = r'(?i)\b{}\b.*?(?=\n\n|\Z)'.format(section)  # Case-insensitive section removal
        text = re.sub(pattern, '', text, flags=re.DOTALL)

    # Remove references to figures, tables, and page numbers
    text = re.sub(r'Figure\s*\d+', '', text)  # Remove "Figure X" references
    text = re.sub(r'Page\s*\d+\s*(of\s*\d+)?', '', text)  # Remove "Page X of Y" references
    text = re.sub(r'Table\s*\d+', '', text)  # Remove "Table X" references
    
    # You can add additional patterns to remove any other sections you don't want
    text = re.sub(r'Gates Open Research\s*\d{4},.*?Last updated:.*?\n', '', text)  # Remove repeated journal info
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces/newlines with a single space
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII characters
    text = remove_leading_zeros(text)
    text = text.strip()
    text = re.sub(r'\. \.', '.', text)  # Fix any erroneous spaces between periods

    # Ensure paragraphs are maintained
    text = re.sub(r'\n\s*\n', '\n\n', text)  # Ensure paragraph breaks are preserved

    return text


# Function to remove leading zeros from numbers
def remove_leading_zeros(text):
    pattern = r'\b0+(\d+(\.\d+)?)\b'
    result = re.sub(pattern, r'\1', text)
    return result


# Function to fix encoding issues
def fix_encoding_issues(text):
    try:
        text = text.encode('latin1').decode('utf-8')
    except UnicodeEncodeError:
        pass  # If encoding fails, just return the original text
    return text


# Function to extract the title if it's the first sentence before author names

def extract_title(text):
    # This regex will capture all text before the "[version" part
    title_match = re.search(r'^(.+?)\s*\[version.*$', text, re.DOTALL)
    if title_match:
        return title_match.group(1).strip()
    return None



# Function to extract DOI
def extract_doi(text):
    # Fix encoding issues
    text = fix_encoding_issues(text)
    
    # Regex pattern to match a DOI
    match = re.search(r'10\.\d{4,9}/[-._;()/:A-Z0-9]+', text, re.IGNORECASE)
    
    if match:
        doi = match.group(0).strip()
        
        # Clean up any trailing or leading non-DOI characters
        doi = re.sub(r'[^a-zA-Z0-9./:-]+$', '', doi)
        
        return doi
    else:
        return ""

# Function to extract authors
def extract_authors(text):
    text = fix_encoding_issues(text)
    # This regex looks for a list of names separated by commas
    match = re.search(r'(?m)^\s*[A-Z][a-z]+(?: [A-Z]\.)?(?:, [A-Z][a-z]+(?: [A-Z]\.)?)*', text)
    return match.group(0).strip() if match else ""

# Function to extract FullTextURL
def extract_fulltexturl(text):
    text = fix_encoding_issues(text)  # Fix any encoding issues first
    
    # Use regex to search for a line that contains 'FulltextUrl:' followed by a valid URL
    match = re.search(r'https?://[^\s]+', text)
    
    if match:
        url = match.group(0).strip()
        
        # Remove any trailing non-URL characters (e.g., 'List')
        url = re.sub(r'[^\w:/?=&.-]+$', '', url)  # Remove trailing non-URL characters
        
        return url
    else:
        return ""
    

def check_pdf_path_exists(pdf_path):
    # Use pathlib for cross-platform compatibility
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    return True


def load_pdf_and_extract_data(pdf_path):
    pdf_path = 'What_is_Sustainability-1.pdf'
    current_dir = Path(__file__).parent
    pdf_path = current_dir / "data" / pdf_path
    
    if check_pdf_path_exists(pdf_path):
        content = ""

        # Extract text from each page in the PDF
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                content += page.extract_text() + " "

    # Extract the required fields using the provided functions
    title = extract_title(content)
    doi = extract_doi(content)
    full_text_url = extract_fulltexturl(content)
    cleaned_content = cleanse_text(content)

    # Display the extracted information
    extracted_data = {
        "Title": title,
        "DOI": doi,
        "FullTextURL": full_text_url,
        "FullTextContent": cleaned_content
    }
    return extracted_data
    
    

if __name__ == "__main__":
    # Load the PDF file
    pdf_path = 'What_is_Sustainability-1.pdf'
    extracted_data = load_pdf_and_extract_data(pdf_path)
    
    # Printing the results
    print("Title:", extracted_data["Title"])
    print("DOI:", extracted_data["DOI"])
    print("FullTextURL:", extracted_data["FullTextURL"])
    #print("\nFullTextContent (first 1000 characters):\n", extracted_data["FullTextContent"][:10000])
    
    # Save extracted data to a .txt file
    output_path = Path(__file__).parent / "data" / "extracted_data.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Title: {extracted_data['Title']}\n")
        f.write(f"DOI: {extracted_data['DOI']}\n")
        f.write(f"FullTextURL: {extracted_data['FullTextURL']}\n\n")
        f.write("FullTextContent:\n")
        f.write(extracted_data["FullTextContent"])
    print(f"\nExtracted data saved to {output_path}")