from flashrank import Ranker, RerankRequest

import config

_ranker = Ranker()


def rerank(question: str, chunks: list[str], top_n: int = config.RERANK_TOP_N) -> list[str]:
    request = RerankRequest(query=question, passages=[{"text": c} for c in chunks])
    results = _ranker.rerank(request)
    return [r["text"] for r in results[:top_n]]
