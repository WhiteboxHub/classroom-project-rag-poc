from pipelines.ingestion_pipeline import IngestionPipeline

def ingest_data():
    pipeline = IngestionPipeline()
    pipeline.run()

if __name__ == "__main__":
    ingest_data()
