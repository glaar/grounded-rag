from flashrank import Ranker, RerankRequest


_ranker = Ranker()


def rerank(question: str, chunks: list[str], top_n: int = 3) -> list[str]:
    request = RerankRequest(query=question, passages=[{"text": c} for c in chunks])
    results = _ranker.rerank(request)
    return [r["text"] for r in results[:top_n]]
