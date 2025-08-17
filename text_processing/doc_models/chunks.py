import re

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class Chunk:
    """
    A chunk object representing a semantically consistent sub text block.
    """
    
    def __init__(self, text, chunk_id=None, block_id=None, embedding=None):
        """
        Initialize a Chunk object.
        
        Args:
            text (str): The text content of the chunk
            chunk_id (int, optional): Unique identifier for the chunk within its block
            block_id (int, optional): ID of the parent block
            embedding (np.array, optional): Pre-computed embedding for the chunk
        """
        self.text = text
        self.chunk_id = chunk_id
        self.block_id = block_id
        self._embedding = embedding
        self._word_count = None
        self._sentences = None
    
    @property
    def word_count(self):
        """Get the word count of the chunk."""
        if self._word_count is None:
            self._word_count = len(self.text.split())
        return self._word_count
    
    @property
    def sentences(self):
        """Get the sentences in the chunk."""
        if self._sentences is None:
            self._sentences = self._split_into_sentences(self.text)
        return self._sentences
    
    @property
    def sentence_count(self):
        """Get the number of sentences in the chunk."""
        return len(self.sentences)
    
    def get_embedding(self, model=None):
        """
        Get or compute the embedding for this chunk.
        
        Args:
            model: SentenceTransformer model to use for embedding
            
        Returns:
            np.array: The embedding vector for this chunk
        """
        if self._embedding is None:
            if model is None:
                model = SentenceTransformer('all-MiniLM-L6-v2')
            self._embedding = model.encode([self.text])[0]
        return self._embedding
    
    def similarity_to(self, other_chunk, model=None):
        """
        Calculate cosine similarity to another chunk.
        
        Args:
            other_chunk (Chunk): Another chunk to compare with
            model: SentenceTransformer model for embeddings
            
        Returns:
            float: Cosine similarity score
        """
        emb1 = self.get_embedding(model).reshape(1, -1)
        emb2 = other_chunk.get_embedding(model).reshape(1, -1)
        return cosine_similarity(emb1, emb2)[0][0]
    
    def preview(self, max_chars=100):
        """
        Get a preview of the chunk text.
        
        Args:
            max_chars (int): Maximum characters to show
            
        Returns:
            str: Truncated text with ellipsis if needed
        """
        if len(self.text) <= max_chars:
            return self.text
        return self.text[:max_chars] + "..."
    
    @staticmethod
    def _split_into_sentences(text):
        """Split text into sentences using regex."""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def __str__(self):
        return f"Chunk({self.chunk_id}): {self.word_count} words - {self.preview(50)}"
    
    def __repr__(self):
        return f"Chunk(chunk_id={self.chunk_id}, block_id={self.block_id}, word_count={self.word_count})"
    
    def __len__(self):
        return self.word_count



    

    


    

    

    

    

    

    

    

