import os

class PromptPipeline:
    def __init__(self):
        self.prompts_dir = "prompts"
        
    def load_prompt(self, filename: str) -> str:
        path = os.path.join(self.prompts_dir, filename)
        with open(path, 'r') as f:
            return f.read().strip()

    def get_system_prompt(self) -> str:
        return self.load_prompt("system_prompt.txt")

    def get_rag_prompt(self, context: str, question: str) -> str:
        template = self.load_prompt("rag_prompt.txt")
        return template.format(context=context, question=question)
