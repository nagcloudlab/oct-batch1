"""Compare with a real pretrained LLM: load a small instruct model and chat with it."""

from transformers import pipeline

MODEL = "HuggingFaceTB/SmolLM2-135M-Instruct"  # ~270 MB download on first run

generator = pipeline("text-generation", model=MODEL)

messages = [{"role": "user", "content": "Explain what a language model is in two sentences."}]
result = generator(messages, max_new_tokens=80, do_sample=False)
print(result[0]["generated_text"][-1]["content"])
