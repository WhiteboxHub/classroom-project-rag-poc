from utils.evals.datasets import load_eval_dataset
from utils.evals.generation_eval import GenerationEval
from utils.logging import setup_logger

logger = setup_logger(__name__)

def run_evals():
    logger.info("Starting evaluations...")
    dataset = load_eval_dataset()
    evaluator = GenerationEval()
    
    for item in dataset:
        # Placeholder loop
        pass
    
    logger.info("Evaluations complete.")

if __name__ == "__main__":
    run_evals()
