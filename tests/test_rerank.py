from utils.rerank import rerank


CHUNKS = [
    "Starbase Omega has a strict policy on crew conduct.",
    "All crew members must undergo a full medical scan every 30 days.",
    "Crew members are entitled to 3 meals per day via the replicator.",
]


def test_rerank_returns_strings():
    results = rerank("crew medical policy", CHUNKS)
    assert all(isinstance(r, str) for r in results)


def test_rerank_respects_top_n():
    results = rerank("crew medical policy", CHUNKS, top_n=2)
    assert len(results) <= 2
