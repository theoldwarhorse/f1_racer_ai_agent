from large_language_models.config import Config
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


class LargeLanguageModelClient(Config):
    def __init__(self):
        pass

    @staticmethod
    def generate(messages: list[dict[str:str]]) -> str:
        return "This is a mock response"


if __name__ == "__main__":
    prompts = [
        {"role": "system", "content": "You are an F1 driver"},
        {"role": "user", "content": "You just won."},
    ]
    large_language_model_client = LargeLanguageModelClient()
    output = large_language_model_client.generate(messages=prompts)
    print(output)
