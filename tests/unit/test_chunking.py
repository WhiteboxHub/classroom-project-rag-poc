import pytest
from utils.chunking import TextChunker

def test_chunking_basic():
    text = "Hello world " * 100
    chunker = TextChunker(chunk_size=50, chunk_overlap=10)
    chunks = chunker.split_text(text)
    assert len(chunks) > 1
    assert isinstance(chunks[0], str)

def test_chunking_empty():
    chunker = TextChunker()
    assert chunker.split_text("") == []
