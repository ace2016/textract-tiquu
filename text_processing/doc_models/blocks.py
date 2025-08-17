


class Block:
    """
    A block object representing a larger text section that can be split into chunks.
    """
    
    def __init__(self, text, block_id=None, start_header=None, end_header=None):
        """
        Initialize a Block object.
        
        Args:
            text (str): The text content of the block
            block_id (int, optional): Unique identifier for the block
            start_header (str, optional): Starting header that defines this block
            end_header (str, optional): Ending header that defines this block
        """
        self.text = text
        self.block_id = block_id
        self.start_header = start_header
        self.end_header = end_header
        self._chunks = None
        self._word_count = None
    
    @property
    def word_count(self):
        """Get the word count of the block."""
        if self._word_count is None:
            self._word_count = len(self.text.split())
        return self._word_count
    
    def create_chunks(self, chunker, min_words=100, max_words=250, similarity_threshold=0.7):
        """
        Split this block into semantic chunks.
        
        Args:
            chunker (SemanticChunker): The chunker to use
            min_words (int): Minimum words per chunk
            max_words (int): Maximum words per chunk
            similarity_threshold (float): Similarity threshold for splitting
            
        Returns:
            List[Chunk]: List of Chunk objects
        """
        self._chunks = chunker.chunk_block(
            self, 
            min_words=min_words, 
            max_words=max_words, 
            similarity_threshold=similarity_threshold
        )
        return self._chunks
    
    @property
    def chunks(self):
        """Get the chunks for this block (if they've been created)."""
        return self._chunks
    

    def preview(self, max_chars=200):
        """
        Get a preview of the block text.
        
        Args:
            max_chars (int): Maximum characters to show
            
        Returns:
            str: Truncated text with ellipsis if needed
        """
        if len(self.text) <= max_chars:
            return self.text
        return self.text[:max_chars] + "..."
    
    def __str__(self):
        chunk_info = f", {len(self._chunks)} chunks" if self._chunks else ""
        return f"Block({self.block_id}): {self.word_count} words{chunk_info} - {self.preview(50)}"
    
    def __repr__(self):
        return f"Block(block_id={self.block_id}, word_count={self.word_count})"
    
    def __len__(self):
        return self.word_count



    