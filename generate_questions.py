import os
import json

from utils.document_loader import load_all_documents
from llm.generate import call_llm  # Your wrapper around openai_client

QUESTION_PROMPT = (
    """Read the following text:\n\n{text}\n\n"""
    "1. Extract all specific facts from the text: dates, names, organizations, technical parameters, etc.\n"
    "2. Then generate two questions:\n\n"
    "- One **positive**: a question that has a clear and precise answer in the text, using at least one of the identified facts.\n"
    "- One **negative**: formulate a realistic question related to the text's topic, but **without using any of the identified facts**. Invent a new fact that sounds plausible but **does not appear in the text**.\n\n"
    "Response format must be strict JSON:\n\n"
    "{\n"
    '  "positive": {\n'
    '    "query": "question",\n'
    '    "expected_keywords": ["key", "word"]\n'
    "  },\n"
    '  "negative": {\n'
    '    "query": "question",\n'
    '    "expected_keywords": []\n'
    "  }\n"
    "}"
)

def generate_questions_for_document(text: str) -> list[dict]:
    prompt = QUESTION_PROMPT.replace("{text}", text.strip())
    result = call_llm(prompt).strip()

    # Remove Markdown block if LLM added it
    if result.startswith("```"):
        result = result.strip("`")
        if result.startswith("json"):
            result = result[len("json"):].strip()

    try:
        parsed = json.loads(result)
        return [
            parsed["positive"],
            parsed["negative"]
        ]
    except Exception as e:
        print(f"⚠️ Failed to parse JSON: {result}\nError: {e}")
        return []

def main():
    documents = load_all_documents("data/source_docs/")
    output_path = "data/queries.jsonl"
    os.makedirs("data", exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for doc in documents:
            print(f"📄 Processing document: {doc['name']}")
            questions = generate_questions_for_document(doc["text"])
            for q in questions:
                f.write(json.dumps(q, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
