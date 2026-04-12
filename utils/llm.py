from ollama import chat
import config


def answer(question: str, context: list[str]) -> str:
    context_text = "\n\n".join(context)
    prompt = f"""Answer the question based only on the context below.

    Context:
    {context_text}

    Question: {question}"""

    response = chat(
        model=config.CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.message.content or ""
