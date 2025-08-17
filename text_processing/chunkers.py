import re

import numpy as np
from rich import print
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from text_processing.doc_models.chunks import Chunk
from text_processing.doc_models.documents import Document


class SemanticChunker:
    """
    A class to split blocks into semantic chunks and return Chunk objects.
    """
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initialize the semantic chunker.
        
        Args:
            model_name (str): Name of the SentenceTransformer model to use
        """
        self.model = SentenceTransformer(model_name)
    
    def chunk_block(self, block, min_words=100, max_words=250, similarity_threshold=0.7):
        """
        Split a Block object into semantic chunks and return Chunk objects.
        
        Args:
            block (Block): Block object to chunk
            min_words (int): Minimum words per chunk
            max_words (int): Maximum words per chunk
            similarity_threshold (float): Similarity threshold for splitting
            
        Returns:
            List[Chunk]: List of Chunk objects
        """
        # Split into sentences
        sentences = self._split_into_sentences(block.text)
        sentence_embeddings = self.model.encode(sentences)
        
        chunks = []
        current_sentences = []
        current_embeddings = []
        current_word_count = 0
        
        for i, sentence in enumerate(sentences):
            sentence_words = len(sentence.split())
            proposed_word_count = current_word_count + sentence_words
            
            # If we're under minimum, must add
            if current_word_count < min_words:
                current_sentences.append(sentence)
                current_embeddings.append(sentence_embeddings[i])
                current_word_count += sentence_words
            
            # If adding would exceed maximum, split now
            elif proposed_word_count > max_words:
                # Save current chunk
                chunk_text = ' '.join(current_sentences)
                chunk_embedding = np.mean(current_embeddings, axis=0)
                chunks.append(Chunk(
                    text=chunk_text, 
                    chunk_id=len(chunks),
                    block_id=block.block_id,
                    embedding=chunk_embedding
                ))
                
                # Start new chunk with current sentence
                current_sentences = [sentence]
                current_embeddings = [sentence_embeddings[i]]
                current_word_count = sentence_words
            
            # We're in the decision zone (between min and max)
            else:
                # Compare new sentence to current chunk average
                chunk_avg_embedding = np.mean(current_embeddings, axis=0)
                similarity = cosine_similarity(
                    sentence_embeddings[i].reshape(1, -1),
                    chunk_avg_embedding.reshape(1, -1)
                )[0][0]
                
                if similarity >= similarity_threshold:
                    # Similar enough, add to current chunk
                    current_sentences.append(sentence)
                    current_embeddings.append(sentence_embeddings[i])
                    current_word_count += sentence_words
                else:
                    # Not similar, split here
                    chunk_text = ' '.join(current_sentences)
                    chunk_embedding = np.mean(current_embeddings, axis=0)
                    chunks.append(Chunk(
                        text=chunk_text,
                        chunk_id=len(chunks),
                        block_id=block.block_id,
                        embedding=chunk_embedding
                    ))
                    
                    # Start new chunk
                    current_sentences = [sentence]
                    current_embeddings = [sentence_embeddings[i]]
                    current_word_count = sentence_words
        
        # Add final chunk if it exists
        if current_sentences:
            chunk_text = ' '.join(current_sentences)
            chunk_embedding = np.mean(current_embeddings, axis=0)
            chunks.append(Chunk(
                text=chunk_text,
                chunk_id=len(chunks),
                block_id=block.block_id,
                embedding=chunk_embedding
            ))
        
        return chunks
    
    @staticmethod
    def _split_into_sentences(text):
        """Split text into sentences using regex."""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]


# Example usage:
if __name__ == "__main__":
    # Initialize chunker
    chunker = SemanticChunker()
    
    # Example markdown text with headers (replace with your actual text)
    sample_text = """
    # Introduction
    This is the introduction section with some content that explains the basics.
    
    ## History of the Concept
    This section contains historical information about the concept.
    It has multiple sentences that provide detailed background.
    The history spans several decades of research and development.
    
    ## People, Planet, Profit
    This section discusses the triple bottom line approach.
    It covers environmental, social, and economic considerations.
    The framework has become widely adopted in business.
    
    ### Implementation Details
    Here we discuss how to implement these concepts.
    There are several steps involved in the process.
    Each step requires careful consideration and planning.
    """
    
    # Create document and process it
    document = Document(sample_text, doc_id="sample_doc")
    
    # Step 1: Split into blocks
    blocks = document.create_blocks(min_words=20)  # Lower threshold for demo
    
    print(f"Document split into {len(blocks)} blocks:")
    for block in blocks:
        print(f"  {block}")
    
    print("\n" + "="*50 + "\n")
    
    # Step 2: Split each block into chunks
    for block in blocks:
        chunks = block.create_chunks(chunker, similarity_threshold=0.45)
        
        print(f"Block {block.block_id} ('{block.start_header}') split into {len(chunks)} chunks:")
        for chunk in chunks:
            print(f"  Chunk {chunk.chunk_id}: {chunk.word_count} words")
            print(f"    {chunk.preview(100)}")
        print()
    
    # Example of getting all chunks from the document
    all_chunks = document.get_all_chunks()
    print(f"Total chunks across all blocks: {len(all_chunks)}")
    
                                                                