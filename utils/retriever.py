import openai
import chromadb
import httpx

from configs.settings import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    USE_PROXY,
    PROXY_URL
)

# Configure custom httpx transport (if proxy is needed)
if USE_PROXY and PROXY_URL:
    transport = httpx.HTTPTransport(proxy=PROXY_URL, verify=False)
    http_client = httpx.Client(transport=transport)
    openai_client = openai.OpenAI(api_key=OPENAI_API_KEY, http_client=http_client)
else:
    openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)


def retrieve_chunks(query: str, config: dict, run_id: str) -> list[str]:
    """
    Performs query embedding using OpenAI and retrieves the closest chunks from ChromaDB.
    """
    top_k = config["retrieval"]["top_k"]
    model = config.get("embedding", {}).get("model", OPENAI_MODEL)

    # Get query embedding
    embedding_response = openai_client.embeddings.create(
        model=model,
        input=query
    )
    query_embedding = embedding_response.data[0].embedding

    # Connect to ChromaDB
    client = chromadb.PersistentClient(path=f"embeddings/{run_id}")
    collection = client.get_or_create_collection("rag_eval")
    print("Total documents in collection:", collection.count())

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents"]
    )

    return results["documents"][0]
