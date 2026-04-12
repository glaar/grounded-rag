from typing import Sequence

import chromadb

from utils.embedding import embed_chunks

def in_memory_vector_store(embeddings: Sequence[Sequence[float]], chunks: list[str]):
    client = chromadb.Client()
    collection = client.get_or_create_collection("my_collection")
    collection.add(
        ids=[str(i) for i in range(len(chunks))],
        embeddings=list(embeddings),
        documents=chunks
    )
    return collection

def query(question: str, collection) -> list[str]:
    query_embeddings = embed_chunks([question]) 
    results = collection.query(query_embeddings=query_embeddings, n_results=3)
    return results["documents"][0]
