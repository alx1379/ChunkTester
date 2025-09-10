import os
import json

from utils.document_loader import load_all_documents
from llm.generate import call_llm  # Твоя обёртка вокруг openai_client

QUESTION_PROMPT = (
    "Прочитай следующий текст:\n\n{text}\n\n"
    "1. Выдели все конкретные факты из текста: даты, фамилии, организации, технические параметры и т.п.\n"
    "2. Затем сгенерируй два вопроса:\n\n"
    "- Один **positive**: на который есть чёткий и точный ответ в тексте, использующий хотя бы один из найденных фактов.\n"
    "- Один **negative**: сформулируй реалистичный вопрос, относящийся к теме текста, но так, чтобы **в нём НЕ использовался ни один из выделенных фактов**. Придумай новый факт, который звучит правдоподобно, но **не встречается в тексте**.\n\n"
    "Формат ответа строго JSON:\n\n"
    "{\n"
    '  "positive": {\n'
    '    "query": "вопрос",\n'
    '    "expected_keywords": ["ключевое", "слово"]\n'
    "  },\n"
    '  "negative": {\n'
    '    "query": "вопрос",\n'
    '    "expected_keywords": []\n'
    "  }\n"
    "}"
)

def generate_questions_for_document(text: str) -> list[dict]:
    prompt = QUESTION_PROMPT.replace("{text}", text.strip())
    result = call_llm(prompt).strip()

    # Убираем Markdown-блок, если LLM его добавил
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
        print(f"⚠️ Не удалось распарсить JSON: {result}\nОшибка: {e}")
        return []

def main():
    documents = load_all_documents("data/source_docs/")
    output_path = "data/queries.jsonl"
    os.makedirs("data", exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for doc in documents:
            print(f"📄 Обработка документа: {doc['name']}")
            questions = generate_questions_for_document(doc["text"])
            for q in questions:
                f.write(json.dumps(q, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
