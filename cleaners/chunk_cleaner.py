import re
from cleaners.heuristics import INSTRUCTION_PATTERNS

def clean_chunk(text: str) -> str:
    """
    Удаляет из текста инструкции, системные фразы, служебные вставки и вводные фразы.
    Используется только если clean_context_instructions = true.
    """
    cleaned = text

    for pattern in INSTRUCTION_PATTERNS:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

    # Убираем множественные пробелы и пустые строки
    cleaned = re.sub(r"\n{2,}", "\n", cleaned)
    cleaned = re.sub(r"[ \t]{2,}", " ", cleaned).strip()

    return cleaned

def clean_chunks(chunks: list[dict]) -> list[dict]:
    """
    Удаляет из чанков строки, которые содержат явные инструкции типа:
    - 'Ответь на этот вопрос:'
    - 'Вопрос:'
    - 'Ты — ассистент...'

    Простой фильтр — можно доработать по регуляркам.
    """
    cleaned = []
    for ch in chunks:
        text = ch["chunk"]
        lines = text.splitlines()
        filtered = [
            line for line in lines
            if not any(bad in line.lower() for bad in ["вопрос:", "ответь", "ты —", "инструкция"])
        ]
        ch["chunk"] = "\n".join(filtered).strip()
        cleaned.append(ch)
    return cleaned

