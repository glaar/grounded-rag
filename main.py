import sys
import config

from utils.ingestion import pdf_to_text, chunk_text
from utils.embedding import embed_chunks

from utils.vector_store import in_memory_vector_store, query


def main(user_input: str | None):
    if user_input == None:
        user_input = config.DEFAULT_QUERY

    # Ingestion
    raw_text = pdf_to_text(config.PDF_PATH)

    # Split text into chunks
    chunks = chunk_text(raw_text, config.CHUNK_SIZE, config.CHUNK_OVERLAP)

    #Embeddings
    embeddings = embed_chunks(chunks)

    #Collection store
    collection = in_memory_vector_store(embeddings, chunks)

    #Fetch relevant chunks
    results = query(user_input, collection)



    


if __name__ == "__main__":
    user_input = sys.argv[1] if len(sys.argv) > 1 else None
    main(user_input)
