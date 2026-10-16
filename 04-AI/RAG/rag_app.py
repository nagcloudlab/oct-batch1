"""RAG chat app: the pipeline from rag_demo.ipynb as one runnable program.

    python rag_app.py                      # interactive chat
    python rag_app.py "What does E-42 mean?"   # one question
    python rag_app.py --reindex            # rebuild the vector DB from data/
"""

import re
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

import chromadb
import numpy as np
import torch
from chromadb.utils import embedding_functions
from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.utils import logging as hf_logging

hf_logging.set_verbosity_error()

DATA_DIR = Path(__file__).parent / "data"
DB_DIR = str(Path(__file__).parent / "chroma_db")
COLLECTION = "nimbus_kb"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
LLM_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"
DEVICE = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"

SYSTEM_PROMPT = (
    "You are a helpful assistant for Nimbus Robotics. Answer the question using ONLY the context below. "
    "Cite the sources you used like [1] or [2]. If the answer is not in the context, say exactly: "
    "\"I don't know based on the provided documents.\""
)


# ---------- indexing ----------

def chunk_document(name, text, max_words=80, overlap=20):
    title = text.splitlines()[0].lstrip("# ").strip()
    chunks = []
    for sec in re.split(r"\n(?=## )", text)[1:]:
        heading, _, body = sec.partition("\n")
        heading = heading.lstrip("# ").strip()
        words = body.split()
        for i, start in enumerate(range(0, max(len(words) - overlap, 1), max_words - overlap)):
            chunks.append({
                "id": f"{name}::{heading}::{i}",
                "text": f"{title} > {heading}\n" + " ".join(words[start:start + max_words]),
                "metadata": {"source": name, "section": heading, "part": i},
            })
    return chunks


def load_chunks():
    return [c for p in sorted(DATA_DIR.glob("*.md")) for c in chunk_document(p.name, p.read_text())]


def get_collection(chunks, reindex=False):
    client = chromadb.PersistentClient(path=DB_DIR)
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL, device=DEVICE)
    if reindex and COLLECTION in [c.name for c in client.list_collections()]:
        client.delete_collection(COLLECTION)
    col = client.get_or_create_collection(COLLECTION, embedding_function=embed_fn, metadata={"hnsw:space": "cosine"})
    if col.count() != len(chunks):  # new or changed documents → (re)index
        print(f"Indexing {len(chunks)} chunks into ChromaDB...")
        col.upsert(ids=[c["id"] for c in chunks], documents=[c["text"] for c in chunks],
                   metadatas=[c["metadata"] for c in chunks])
    return col


# ---------- retrieval ----------

class Retriever:
    def __init__(self, chunks, collection):
        self.col = collection
        self.by_id = {c["id"]: c for c in chunks}
        self.ids = [c["id"] for c in chunks]
        self.bm25 = BM25Okapi([self._tok(c["text"]) for c in chunks])
        self.reranker = CrossEncoder(RERANK_MODEL, device=DEVICE)

    @staticmethod
    def _tok(s):
        return re.findall(r"[a-z0-9\-]+", s.lower())

    def retrieve(self, query, pool=10, top_n=3):
        vector = self.col.query(query_texts=[query], n_results=pool)["ids"][0]
        keyword = [self.ids[i] for i in np.argsort(self.bm25.get_scores(self._tok(query)))[::-1][:pool]]
        fused = {}
        for ranking in (vector, keyword):  # Reciprocal Rank Fusion
            for rank, id_ in enumerate(ranking):
                fused[id_] = fused.get(id_, 0) + 1 / (60 + rank + 1)
        candidates = [self.by_id[i] for i in sorted(fused, key=fused.get, reverse=True)[:pool]]
        scores = self.reranker.predict([(query, c["text"]) for c in candidates], show_progress_bar=False)
        order = np.argsort(scores)[::-1][:top_n]
        return [candidates[i] for i in order]


# ---------- generation ----------

class Generator:
    def __init__(self):
        self.tok = AutoTokenizer.from_pretrained(LLM_MODEL)
        dtype = torch.float16 if DEVICE != "cpu" else torch.float32
        self.llm = AutoModelForCausalLM.from_pretrained(LLM_MODEL, dtype=dtype).to(DEVICE)

    def answer(self, question, hits, max_new_tokens=250):
        context = "\n\n".join(f"[{i}] ({h['metadata']['source']} › {h['metadata']['section']})\n{h['text']}"
                              for i, h in enumerate(hits, 1))
        messages = [{"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}]
        prompt = self.tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.tok(prompt, return_tensors="pt").to(DEVICE)
        with torch.no_grad():
            out = self.llm.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False,
                                    temperature=None, top_p=None, top_k=None)
        return self.tok.decode(out[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()


def main():
    args = sys.argv[1:]
    reindex = "--reindex" in args
    args = [a for a in args if a != "--reindex"]

    print(f"Loading models on {DEVICE}...")
    chunks = load_chunks()
    retriever = Retriever(chunks, get_collection(chunks, reindex))
    generator = Generator()

    def ask(q):
        hits = retriever.retrieve(q)
        print("\n" + generator.answer(q, hits))
        print("\nSources:")
        for i, h in enumerate(hits, 1):
            print(f"  [{i}] {h['metadata']['source']} › {h['metadata']['section']}")

    if args:
        ask(" ".join(args))
        return
    print("\nAsk about Nimbus Robotics (type 'exit' to quit).")
    while True:
        try:
            q = input("\n❓ ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if q.lower() in {"exit", "quit"}:
            break
        if q:
            ask(q)


if __name__ == "__main__":
    main()
