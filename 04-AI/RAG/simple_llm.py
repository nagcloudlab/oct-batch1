"""Simple LLM demo: build a tiny GPT-style model with Transformers, train it, run it."""

import torch
from transformers import GPT2Config, GPT2LMHeadModel, GPT2TokenizerFast

torch.manual_seed(0)

# Training data: a tiny corpus the model will learn to reproduce.
TEXT = """
The cat sat on the mat. The dog sat on the rug.
The cat likes milk. The dog likes bones.
A language model predicts the next word in a sentence.
Transformers use attention to look at earlier words.
""" * 20

# 1. Tokenizer: reuse GPT-2's pretrained tokenizer (only the vocabulary, not the weights).
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

# 2. Build the model from scratch: a very small GPT-2 with random weights.
config = GPT2Config(
    vocab_size=tokenizer.vocab_size,
    n_positions=128,  # max context length
    n_embd=128,       # hidden size
    n_layer=2,        # transformer blocks
    n_head=4,         # attention heads
)
model = GPT2LMHeadModel(config)
print(f"Model parameters: {model.num_parameters():,}")

# 3. Train: next-token prediction on random 64-token windows of the corpus.
ids = tokenizer(TEXT, return_tensors="pt").input_ids[0]
block, batch_size, steps = 64, 8, 300
optimizer = torch.optim.AdamW(model.parameters(), lr=3e-3)

model.train()
for step in range(steps):
    starts = torch.randint(0, len(ids) - block, (batch_size,))
    batch = torch.stack([ids[s : s + block] for s in starts])
    loss = model(input_ids=batch, labels=batch).loss  # labels are shifted internally
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
    if step % 50 == 0 or step == steps - 1:
        print(f"step {step:3d}  loss {loss.item():.3f}")

# 4. Run: generate text from a few prompts.
model.eval()
for prompt in ["The cat", "The dog", "A language model"]:
    inputs = tokenizer(prompt, return_tensors="pt")
    out = model.generate(
        **inputs,
        max_new_tokens=15,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id,
    )
    print(f"\n> {prompt}\n{tokenizer.decode(out[0], skip_special_tokens=True)}")
