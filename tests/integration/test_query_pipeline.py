import unittest
from unittest.mock import patch, MagicMock
from pipelines.query_pipeline import QueryPipeline

class TestQueryPipelineIntegration(unittest.TestCase):
    @patch('pipelines.query_pipeline.create_retrieval_chain')
    @patch('pipelines.query_pipeline.create_stuff_documents_chain')
    @patch('pipelines.query_pipeline.get_vectorstore')
    @patch('pipelines.query_pipeline.get_llm')
    def test_run_query_flow(self, mock_get_llm, mock_get_vstore, mock_stuff_chain, mock_retrieval_chain):
        # Mock final chain invocation
        mock_chain_instance = MagicMock()
        mock_chain_instance.invoke.return_value = {
            "answer": "The Answer",
            "context": [MagicMock(page_content="Content", metadata={})]
        }
        mock_retrieval_chain.return_value = mock_chain_instance
        
        # Run
        pipeline = QueryPipeline()
        answer, sources = pipeline.run("Question")
        
        # Verify
        self.assertEqual(answer, "The Answer")
        self.assertEqual(len(sources), 1)
        mock_chain_instance.invoke.assert_called_with({"input": "Question"})
