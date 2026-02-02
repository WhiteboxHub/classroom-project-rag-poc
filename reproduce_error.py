import sys
import os
# Add the project root to sys.path
sys.path.append(os.getcwd())

try:
    from pipelines.query_pipeline import QueryPipeline
    from utils.config import Config
    
    # Mock Config if necessary, but we'll try to run with real env
    pipeline = QueryPipeline()
    print("Pipeline initialized.")
    
    # Test with a dummy query
    # We expect an error if OpenAI key is invalid, but not a NameError
    try:
        answer, sources = pipeline.run("What is the provider manual?", stream=False)
        print("Run complete.")
        print(f"Answer: {answer[:100]}...")
    except Exception as e:
        print(f"Caught expected error or bug: {e}")
        import traceback
        traceback.print_exc()

except Exception as e:
    print(f"Initialization error: {e}")
    import traceback
    traceback.print_exc()
