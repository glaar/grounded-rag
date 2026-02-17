import sys
import config

from utils.ingestion import pdf_to_text

from ollama import chat

def main(query: str | None):
    if query == None:
        query = config.DEFAULT_QUERY

    # Ingestion step
    raw_text = pdf_to_text(config.PDF_PATH)
    print(raw_text)

    response = chat(
        model=config.CHAT_MODEL,
        messages=[
            {
                "role": "user",
                "content": query
            }
        ],
    )

    answer = response.message.content or ""
    print(answer)


if __name__ == "__main__":
    user_input = sys.argv[1] if len(sys.argv) > 1 else None
    main(user_input)
