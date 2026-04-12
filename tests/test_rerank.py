from utils.rerank import rerank


CHUNKS = [
    "Northwind Wizardry has a strict policy on employee conduct.",
    "All employees must submit expense reports within 30 days.",
    "Employees are entitled to 25 days of annual leave.",
]


def test_rerank_returns_strings():
    results = rerank("employee policy", CHUNKS)
    assert all(isinstance(r, str) for r in results)


def test_rerank_respects_top_n():
    results = rerank("employee policy", CHUNKS, top_n=2)
    assert len(results) <= 2
