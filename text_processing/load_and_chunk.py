import os

from marker.config.parser import ConfigParser
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict

from text_processing.chunkers import SemanticChunker
from text_processing.doc_models.documents import Document


def pdf2markdown(file_path, output_format="markdown"):

    config = {
        "output_format": output_format,
        "ADDITIONAL_KEY": "VALUE"
    }
    config_parser = ConfigParser(config)

    converter = PdfConverter(
        config=config_parser.generate_config_dict(),
        artifact_dict=create_model_dict(),
        processor_list=config_parser.get_processors(),
        renderer=config_parser.get_renderer(),
        llm_service=config_parser.get_llm_service()
    )

    rendered_file = converter(filepath=str(file_path))
    return rendered_file


def process_and_chunk_document(file_path, similarity_threshold=0.45):
    # Extract text from the rendered file
    rendered_file = pdf2markdown(file_path)
    sample_text = rendered_file.markdown

    # Create document and process it
    document = Document(sample_text, doc_id="sample_doc")
    
    # Step 1: Split into blocks
    blocks = document.create_blocks(min_words=150)  # Lower threshold for demo
        
    # Step 2: Split each block into chunks
    chunker = SemanticChunker()
    for block in blocks:
        chunks = block.create_chunks(chunker, similarity_threshold=0.45)
        
        # Prepare output directory and file path
        output_dir = "data/results"
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(
            output_dir,
            os.path.splitext(os.path.basename(file_path))[0] + "_chunks.txt"
        )

        # Collect result strings
        result_lines = []
        result_lines.append(f"Block {block.block_id} ('{block.start_header}') split into {len(chunks)} chunks:")
        for chunk in chunks:
            result_lines.append(f"  Chunk {chunk.chunk_id}: {chunk.word_count} words")
            result_lines.append(chunk.text)
            result_lines.append("")  # Separate chunks

        result_lines.append("")  # Separate blocks

        # Write results to file (append mode)
        with open(output_file, "a", encoding="utf-8") as f:
            f.write("\n".join(result_lines))
        print(f"Processed and chunked document saved to: {output_file}")

    return document