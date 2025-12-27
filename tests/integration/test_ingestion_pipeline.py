import unittest
from unittest.mock import patch, MagicMock
from pipelines.ingestion_pipeline import IngestionPipeline

class TestIngestionPipelineIntegration(unittest.TestCase):
    @patch('pipelines.ingestion_pipeline.get_vectorstore')
    @patch('pipelines.ingestion_pipeline.PyPDFLoader')
    @patch('pipelines.ingestion_pipeline.RecursiveCharacterTextSplitter')
    def test_run_ingestion_flow(self, mock_splitter_cls, mock_loader_cls, mock_get_vstore):
        # Mock Loader
        mock_loader = MagicMock()
        mock_loader.load.return_value = ["doc1"]
        mock_loader_cls.return_value = mock_loader
        
        # Mock Splitter
        mock_splitter = MagicMock()
        mock_splitter.split_documents.return_value = ["chunk1", "chunk2"]
        mock_splitter_cls.return_value = mock_splitter
        
        # Mock Vectorstore
        mock_vstore = MagicMock()
        mock_get_vstore.return_value = mock_vstore
        
        # Run
        pipeline = IngestionPipeline()
        pipeline.run()
        
        # Verify
        mock_loader.load.assert_called_once()
        mock_splitter.split_documents.assert_called_with(["doc1"])
        mock_vstore.add_documents.assert_called_with(["chunk1", "chunk2"])
