import unittest
from unittest.mock import patch, MagicMock
from utils.evals.generation_eval import GenerationEval

class TestGenerationEval(unittest.TestCase):
    @patch('utils.evals.generation_eval.LLMGenerator')
    def test_evaluate_response(self, mock_llm_cls):
        mock_llm = MagicMock()
        mock_llm.generate.return_value = '{"faithfulness": 5, "relevance": 5}'
        mock_llm_cls.return_value = mock_llm
        
        evaluator = GenerationEval()
        result = evaluator.evaluate_response("Context", "Question", "Answer")
        
        self.assertIn("faithfulness", result)
