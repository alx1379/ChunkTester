from llm.generate import openai_client, stats

def embed_chunks(texts: list[str], model: str = "text-embedding-3-small") -> list[list[float]]:
    response = openai_client.embeddings.create(
        model=model,
        input=texts
    )

    if response.usage:
        stats["embed_tokens"] += response.usage.total_tokens
        stats["calls"] += 1

    return [item.embedding for item in response.data]
