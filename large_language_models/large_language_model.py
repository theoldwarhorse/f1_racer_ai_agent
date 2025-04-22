from large_language_models.config import Config
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


class LargeLanguageModelClient(Config):
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.model)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model,
            device_map="auto",
            torch_dtype=torch.bfloat16,
        )
        self.messages = []

    def generate(self, messages: list[dict[str:str]]) -> str:
        tokenized_chat = self.tokenizer.apply_chat_template(
            messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
        )
        outputs = self.model.generate(tokenized_chat, max_new_tokens=60, pad_token_id=1)
        return self.tokenizer.decode(outputs[-1]).split("<|assistant|>")[-1]


if __name__ == "__main__":
    prompts = [
        {"role": "system", "content": "You are an F1 driver"},
        {"role": "user", "content": "You just won."},
    ]
    large_language_model_client = LargeLanguageModelClient()
    output = large_language_model_client.generate(messages=prompts)
    print(output)
