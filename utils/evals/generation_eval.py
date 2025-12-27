from utils.llm import LLMGenerator
from pipelines.prompt_pipeline import PromptPipeline
import json

class GenerationEval:
    def __init__(self):
        self.llm = LLMGenerator()
        self.prompt_pipeline = PromptPipeline()

    def evaluate_response(self, context, question, answer):
        # Use LLM to grade itself
        # This is a very basic implementation
        prompt_template = self.prompt_pipeline.load_prompt("eval_prompt.txt")
        prompt = prompt_template.format(context=context, question=question, answer=answer)
        
        response = self.llm.generate([{"role": "user", "content": prompt}])
        return response
