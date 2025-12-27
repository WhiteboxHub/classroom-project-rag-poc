from typing import List
import tiktoken
from utils.config import Config
from utils.logging import setup_logger

logger = setup_logger(__name__)

class TextChunker:
    def __init__(self, chunk_size: int = Config.CHUNK_SIZE, chunk_overlap: int = Config.CHUNK_OVERLAP):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.tokenizer = tiktoken.get_encoding("cl100k_base") # encoding for gpt-4

    def split_text(self, text: str) -> List[str]:
        tokens = self.tokenizer.encode(text)
        if not tokens:
            return []
        
        chunks = []
        start = 0
        total_tokens = len(tokens)
        
        while start < total_tokens:
            end = min(start + self.chunk_size, total_tokens)
            chunk_tokens = tokens[start:end]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            chunks.append(chunk_text)
            
            if end == total_tokens:
                break
                
            start += (self.chunk_size - self.chunk_overlap)
            
        logger.debug(f"Split text into {len(chunks)} chunks")
        return chunks
