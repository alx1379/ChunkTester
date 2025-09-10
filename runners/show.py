# runners/show.py

import json
from pathlib import Path

def show_fails(run_id: str = None):
    print("📉 Показ неудачных ответов (score ≤ 0)")

    if run_id is None:
        try:
            with open("embeddings/run_id.txt", "r", encoding="utf-8") as f:
                run_id = f.read().strip()
        except FileNotFoundError:
            raise ValueError("❌ run_id не передан и не найден файл embeddings/run_id.txt")

    file_path = Path(f"results/{run_id}/answers.jsonl")
    if not file_path.exists():
        raise FileNotFoundError(f"❌ Файл результатов не найден: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        bad_results = [
            json.loads(line) for line in f
            if line.strip() and json.loads(line)["score"] <= 0
        ]

    print(f"🔍 Найдено плохих ответов: {len(bad_results)}\n")

    for r in bad_results:
        print("❓", r["query"])
        print("🧠", r["answer"])
        print("📌", f"score = {r['score']}")
        print("📚 chunks:", r["retrieved_chunks"][:5], "...\n")  # Можно расширить
