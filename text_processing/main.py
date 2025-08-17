import os
import sys
from pathlib import Path

from text_processing.load_and_chunk import process_and_chunk_document


def runner():
    # change filepath
    file_path = Path(os.getcwd()) / "data/sample_pdf/What_is_Sustainability-1.pdf"
    document = process_and_chunk_document(file_path, similarity_threshold=0.45)
    print(document)
    all_chunks = document.get_all_chunks()
    print(f"Total chunks created: {len(all_chunks)}")

if __name__ == "__main__":
    runner()