import unittest
from unittest.mock import patch, MagicMock
from utils.embedding import EmbeddingGenerator, get_embedding_function

class TestEmbeddingGenerator(unittest.TestCase):
    @patch('utils.embedding.HuggingFaceEmbeddings')
    def test_singleton_initialization(self, mock_hf_embeddings):
        EmbeddingGenerator._instance = None
        
        gen1 = EmbeddingGenerator()
        gen2 = EmbeddingGenerator()
        
        self.assertIs(gen1, gen2)
        mock_hf_embeddings.assert_called_once()

    @patch('utils.embedding.HuggingFaceEmbeddings')
    def test_get_function(self, mock_hf_embeddings):
        EmbeddingGenerator._instance = None
        mock_instance = MagicMock()
        mock_hf_embeddings.return_value = mock_instance
        
        fn = get_embedding_function()
        self.assertEqual(fn, mock_instance)
