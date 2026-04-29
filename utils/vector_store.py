from typing import Sequence

import chromadb

import config
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
    results = collection.query(query_embeddings=query_embeddings, n_results=config.TOP_K)
    return results["documents"][0]
