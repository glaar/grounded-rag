import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import config
from utils.ingestion import pdf_to_text, chunk_text
from utils.embedding import embed_chunks
from utils.vector_store import in_memory_vector_store, query
from utils.rerank import rerank
from utils.llm import answer
from eval.dataset import EVAL_DATASET


def build_pipeline():
    raw_text = pdf_to_text(config.PDF_PATH)
    chunks = chunk_text(raw_text, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
    embeddings = embed_chunks(chunks)
    collection = in_memory_vector_store(embeddings, chunks)
    return collection


def eval_loop(entries, get_response):
    passed = 0
    failed = 0
    for entry in entries:
        question = entry["question"]
        expected = entry["expected"]
        response = get_response(question)
        ok = expected.lower() in response.lower()
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {question}")
        if not ok:
            print(f"       expected: {expected!r}")
            print(f"       got:      {response.strip()}")
        if ok:
            passed += 1
        else:
            failed += 1
    return passed, passed + failed


def run_eval():
    collection = build_pipeline()

    print("=== With RAG context ===")
    def with_context(question):
        candidates = query(question, collection)
        reranked = rerank(question, candidates)
        return answer(question, reranked)

    passed, total = eval_loop(EVAL_DATASET, with_context)
    print(f"\n{passed}/{total} passed")

    print("\n=== Without context (LLM only) ===")
    passed, total = eval_loop(EVAL_DATASET, lambda q: answer(q, []))
    print(f"\n{passed}/{total} passed")


if __name__ == "__main__":
    run_eval()
