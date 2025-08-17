import re

from text_processing.doc_models.blocks import Block


class Document:
    """
    A document object that contains multiple blocks.
    """
    
    def __init__(self, text, doc_id=None):
        """
        Initialize a Document object.
        
        Args:
            text (str): The full text content of the document
            doc_id (str, optional): Unique identifier for the document
        """
        self.text = text
        self.doc_id = doc_id
        self._blocks = None
        self._word_count = None
        
    @property
    def word_count(self):
        """Get the word count of the document."""
        if self._word_count is None:
            self._word_count = len(self.text.split())
        return self._word_count
    
    def create_blocks(self, min_words=150):
        """
        Split document into blocks based on headers.
        
        Args:
            min_words (int): Minimum words per block
            
        Returns:
            List[Block]: List of Block objects
        """
        valid_pairs = self._find_valid_header_pairs(self.text, min_words)
        self._blocks = []
        
        for i, (start_header, end_header, content) in enumerate(valid_pairs):
            block = Block(
                text=content,
                block_id=i,
                start_header=start_header,
                end_header=end_header
            )
            self._blocks.append(block)
        
        return self._blocks
    
    @property
    def blocks(self):
        """Get the blocks for this document (if they've been created)."""
        return self._blocks
    
    def get_all_chunks(self):
        """Get all chunks from all blocks."""
        all_chunks = []
        if self._blocks:
            for block in self._blocks:
                if block.chunks:
                    all_chunks.extend(block.chunks)
        return all_chunks
    
    # Header extraction and validation methods (from your original code)
    def _extract_headers(self, markdown_text):
        """Extract headers 1-10 (# ## ### #### etc.)"""
        pattern = r'^(#{1,10})\s+(.+)$'
        headers = []
        for line in markdown_text.split('\n'):
            match = re.match(pattern, line.strip())
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()
                headers.append({'level': level, 'title': title})
        return headers
    
    def _is_valid_header(self, header_text):
        """Check if a header is valid based on heuristics."""
        if not header_text or not header_text.strip():
            return False
        
        clean_text = header_text.replace('*', '').replace('#', '').strip()
        
        if len(clean_text) == 0 or len(clean_text) > 200:
            return False
        
        invalid_patterns = [
            r'<[^>]*>',  # HTML/XML tags
            r'[**\\\/**]',  # Contains backslash or forward slash
            r"[']",  # Contains single quotes
        ]
        
        for pattern in invalid_patterns:
            if re.search(pattern, clean_text, re.IGNORECASE):
                return False
        
        return True
    
    def _extract_between_headers(self, text, start_header, end_header):
        """Extract text between two headers."""
        start_pos = text.find(start_header)
        if start_pos == -1:
            return None
        
        start_pos += len(start_header)
        end_pos = text.find(end_header, start_pos)
        if end_pos == -1:
            return None
        
        extracted = text[start_pos:end_pos].strip()
        
        # Remove markdown headers at the end
        lines = extracted.split('\n')
        while lines and lines[-1].strip().startswith('#'):
            lines.pop()
        
        return '\n'.join(lines).strip()


    def _find_valid_header_pairs(self, text, min_words=50):
        """Find pairs of valid headers with sufficient text between them."""
        all_headers = self._extract_headers(text)
        valid_pairs = []
        i = 0
        
        while i < len(all_headers):
            # Find next valid start header
            start_idx = i
            while start_idx < len(all_headers) and not self._is_valid_header(all_headers[start_idx]['title']):
                start_idx += 1
            
            if start_idx >= len(all_headers):
                break
            
            start_header = all_headers[start_idx]['title']
            
            # Find next valid end header
            end_idx = start_idx + 1
            while end_idx < len(all_headers) and not self._is_valid_header(all_headers[end_idx]['title']):
                end_idx += 1
            
            if end_idx >= len(all_headers):
                break
            
            end_header = all_headers[end_idx]['title']
            
            # Extract text between headers
            extracted_text = self._extract_between_headers(text, start_header, end_header)
            if extracted_text and len(extracted_text.split()) >= min_words:
                valid_pairs.append((start_header, end_header, extracted_text))
            
            i = end_idx
        
        return valid_pairs
    
    def __str__(self):
        block_info = f", {len(self._blocks)} blocks" if self._blocks else ""
        return f"Document({self.doc_id}): {self.word_count} words{block_info}"
    
    def __repr__(self):
        return f"Document(doc_id={self.doc_id}, word_count={self.word_count})"
