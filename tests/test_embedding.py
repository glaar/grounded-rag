import config

def test_embed_chunks(chunks, embeddings):
    assert len(embeddings) == len(chunks), "Number of embeddings should match number of chunks"
    assert len(embeddings[0]) == config.EMBEDDING_DIMENSIONS, "Number of dimensions should match model"
