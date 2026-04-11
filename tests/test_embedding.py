import config
from utils.embedding import embed_chunks

def test_embed_chunks():
    chunks = ["This is first chunk", "This is the second chunk"]
    result = embed_chunks(chunks)

    assert len(result) == 2, "Number of embeddings should match number of chunks"
    assert len(result[0]) == config.EMBEDDING_DIMENSIONS, "Number of dimensions should match model"
