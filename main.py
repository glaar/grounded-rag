import sys
import config

from utils.ingestion import pdf_to_text, chunk_text
from utils.embedding import embed_chunks

from ollama import chat


def main(query: str | None):
    if query == None:
        query = config.DEFAULT_QUERY

    # Ingestion
    raw_text = pdf_to_text(config.PDF_PATH)

    # Split text into chunks
    chunks = chunk_text(raw_text, config.CHUNK_SIZE, config.CHUNK_OVERLAP)

    #Embeddings
    result = embed_chunks(chunks)
    print(type(result))


if __name__ == "__main__":
    user_input = sys.argv[1] if len(sys.argv) > 1 else None
    main(user_input)
