import unittest
from unittest.mock import patch, MagicMock
from utils.llm import get_llm

class TestLLMGenerator(unittest.TestCase):
    @patch('utils.llm.ChatOpenAI')
    def test_get_llm_initialization(self, mock_chat_openai):
        # Test that get_llm instantiates ChatOpenAI correctly
        get_llm()
        mock_chat_openai.assert_called_once()

    @patch('utils.llm.ChatOpenAI')
    def test_generate_call(self, mock_chat_openai):
        # Test wrapper logic if any - currently get_llm returns the instance
        mock_instance = MagicMock()
        mock_chat_openai.return_value = mock_instance
        
        llm = get_llm()
        llm.invoke("Hello")
        
        mock_instance.invoke.assert_called_with("Hello")
