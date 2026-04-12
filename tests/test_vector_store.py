from utils.vector_store import query


def test_in_memory_vector_store(collection, chunks):
    assert collection.count() == len(chunks)


def test_query(collection):
    results = query("hello", collection=collection)

    assert len(results) > 0, "Should return at least one result"
    assert isinstance(results[0], str), "Results should be strings"
