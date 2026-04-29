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
    return collection, chunks


def precision_at_k(retrieved_ids, relevant_ids, k):
    top_k = retrieved_ids[:k]
    if not top_k:
        return 0.0
    return len(set(top_k) & set(relevant_ids)) / len(top_k)


def recall_at_k(retrieved_ids, relevant_ids, k):
    if not relevant_ids:
        return None
    top_k = retrieved_ids[:k]
    return len(set(top_k) & set(relevant_ids)) / len(set(relevant_ids))


def hit_at_k(retrieved_ids, relevant_ids, k):
    top_k = retrieved_ids[:k]
    return int(bool(set(top_k) & set(relevant_ids)))


def reciprocal_rank(retrieved_ids, relevant_ids):
    relevant_set = set(relevant_ids)
    for rank, chunk_id in enumerate(retrieved_ids, start=1):
        if chunk_id in relevant_set:
            return 1 / rank
    return 0.0


def mean(values):
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else 0.0


def compute_metrics(retrieved_ids, relevant_ids, k):
    return {
        "precision": precision_at_k(retrieved_ids, relevant_ids, k),
        "recall": recall_at_k(retrieved_ids, relevant_ids, k),
        "hit": hit_at_k(retrieved_ids, relevant_ids, k),
        "rr": reciprocal_rank(retrieved_ids, relevant_ids),
    }


def print_metrics(label, scores, k):
    print(f"\n{label}")
    print(f"  Precision@{k}:  {mean([s['precision'] for s in scores]):.3f}")
    print(f"  Recall@{k}:     {mean([s['recall'] for s in scores]):.3f}")
    print(f"  Hit Rate@{k}:   {mean([s['hit'] for s in scores]):.3f}")
    print(f"  MRR:            {mean([s['rr'] for s in scores]):.3f}")


def eval_retrieval(entries, chunks, collection, k=config.TOP_K, rerank_k=config.RERANK_TOP_N):
    before_scores, after_scores = [], []

    for entry in entries:
        relevant_ids = entry.get("chunk_with_answer", [])
        candidates = query(entry["question"], collection)
        candidate_ids = [chunks.index(c) for c in candidates if c in chunks]
        before_scores.append(compute_metrics(candidate_ids, relevant_ids, k))

        reranked = rerank(entry["question"], candidates)
        reranked_ids = [chunks.index(c) for c in reranked if c in chunks]
        after_scores.append(compute_metrics(reranked_ids, relevant_ids, rerank_k))

    print_metrics("Before rerank:", before_scores, k)
    print_metrics("After rerank:", after_scores, rerank_k)


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
    collection, chunks = build_pipeline()

    factual = [e for e in EVAL_DATASET if e["expected"] != "cannot"]
    unanswerable = [e for e in EVAL_DATASET if e["expected"] == "cannot"]

    def with_context(question):
        candidates = query(question, collection)
        reranked = rerank(question, candidates)
        return answer(question, reranked)

    print("=== Retrieval quality ===")
    eval_retrieval(factual, chunks, collection)

    print("\n=== Factual accuracy (with RAG context) ===")
    passed, total = eval_loop(factual, with_context)
    print(f"\n{passed}/{total} passed")

    print("\n=== Hallucination resistance (with RAG context) ===")
    passed, total = eval_loop(unanswerable, with_context)
    print(f"\n{passed}/{total} passed")

    print("\n=== Hallucination resistance (no context) ===")
    passed, total = eval_loop(unanswerable, lambda q: answer(q, []))
    print(f"\n{passed}/{total} passed")


if __name__ == "__main__":
    run_eval()
