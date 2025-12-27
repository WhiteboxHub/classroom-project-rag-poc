import unittest
from unittest.mock import patch, MagicMock
from utils.chromadb_client import get_vectorstore

class TestChromaClient(unittest.TestCase):
    @patch('utils.chromadb_client.Chroma')
    @patch('utils.chromadb_client.chromadb.HttpClient')
    @patch('utils.chromadb_client.get_embedding_function')
    def test_get_vectorstore(self, mock_get_embed, mock_http_client, mock_chroma):
        # Verify it initializes LangChain Chroma wrapper
        get_vectorstore()
        mock_chroma.assert_called_once()
