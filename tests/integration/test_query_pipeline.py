import unittest
from unittest.mock import patch, MagicMock
from pipelines.query_pipeline import QueryPipeline

class TestQueryPipelineIntegration(unittest.TestCase):
    @patch('pipelines.query_pipeline.create_stuff_documents_chain')
    @patch('pipelines.query_pipeline.get_vectorstore')
    @patch('pipelines.query_pipeline.get_llm')
    def test_run_query_flow(self, mock_get_llm, mock_get_vstore, mock_stuff_chain):
        # 1. Mock Vectorstore/Retriever
        mock_retriever = MagicMock()
        mock_doc = MagicMock(page_content="Content", metadata={"page": 1})
        mock_retriever.invoke.return_value = [mock_doc]
        
        mock_vstore = MagicMock()
        mock_vstore.as_retriever.return_value = mock_retriever
        mock_get_vstore.return_value = mock_vstore
        
        # 2. Mock LLM Response
        mock_llm = MagicMock()
        mock_response = MagicMock(content="The Answer")
        mock_llm.invoke.return_value = mock_response
        mock_get_llm.return_value = mock_llm
        
        # Run
        pipeline = QueryPipeline()
        answer, sources = pipeline.run("What is the provider manual?", stream=False)
        
        # Verify
        self.assertEqual(answer, "The Answer")
        self.assertEqual(len(sources), 1)
        self.assertEqual(sources[0]["content"], "Content")
        mock_retriever.invoke.assert_called()

    @patch('pipelines.query_pipeline.get_vectorstore')
    @patch('pipelines.query_pipeline.get_llm')
    def test_run_query_streaming(self, mock_get_llm, mock_get_vstore):
        # 1. Mock Vectorstore/Retriever
        mock_retriever = MagicMock()
        mock_doc = MagicMock(page_content="Content", metadata={"page": 1})
        mock_retriever.invoke.return_value = [mock_doc]
        
        mock_vstore = MagicMock()
        mock_vstore.as_retriever.return_value = mock_retriever
        mock_get_vstore.return_value = mock_vstore
        
        # 2. Mock LLM Streaming
        mock_llm = MagicMock()
        mock_chunk = MagicMock(content="Streamed Part")
        mock_llm.stream.return_value = [mock_chunk]
        mock_get_llm.return_value = mock_llm
        
        # Run
        pipeline = QueryPipeline()
        # Ensure query has at least 3 words to pass the guard
        stream, sources = pipeline.run("Tell me about providers in the manual", stream=True)
        
        # Verify
        chunks = list(stream)
        self.assertEqual(chunks[0].content, "Streamed Part")
        self.assertEqual(len(sources), 1)
        mock_llm.stream.assert_called()
