import config
from collections.abc import Sequence
from ollama import embed

def embed_chunks(chunks: list[str]) -> Sequence[Sequence[float]]:
    response = embed(model=config.EMBEDDING_MODEL, input=chunks)
    return response.embeddings
