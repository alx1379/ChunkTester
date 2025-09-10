import json
import os
from pathlib import Path
from tqdm import tqdm
import yaml
from collections import OrderedDict

from utils.retriever import retrieve_chunks
from llm.generate import generate_llm_answer
from scorers.llm_scorer import score_answer_llm, score_answer_llm_negative
from utils.metrics import compute_metrics
from prompts.base import PROMPT_TEMPLATE

from llm.generate import stats  # stats = {"total_tokens": 0, "calls": 0}


def run_eval(config: dict, run_id: str = None, query_file: str = "data/queries.jsonl"):
    print("\n🧪 Start evaluation")

    if run_id is None:
        try:
            with open("embeddings/run_id.txt", "r", encoding="utf-8") as f:
                run_id = f.read().strip()
        except FileNotFoundError:
            raise ValueError("❌ run_id не передан и не найден файл embeddings/run_id.txt")

    output_dir = Path(f"results/{run_id}")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Загружаем вопросы
    with open(query_file, "r", encoding="utf-8") as f:
        queries = [json.loads(line) for line in f if line.strip()]

    results = []
    failed = []
    success = []
    history = []
    history_len = config.get("dialog_history", 0)

    for q in tqdm(queries, desc="Evaluating"):
        query = q["query"]
        expected = q["expected_keywords"]

        # 1. Retrieve chunks
        retrieved = retrieve_chunks(query, config, run_id)
        print(f"🔍 Retrieved {len(retrieved)} chunks for query: {query}")

        # 2. Build prompt (with optional history)
        context = "\n".join(retrieved)
        if history_len > 0:
            prev_messages = "\n".join(history[-history_len:])
            context = prev_messages + "\n\n" + context

        prompt = PROMPT_TEMPLATE.format(context=context, query=query)

        # 3. Generate answer from LLM
        answer = generate_llm_answer(prompt)

        # 4. Score the answer
        if not expected:  # это негативный вопрос
            score = score_answer_llm_negative(query, answer, retrieved)
        else:
            score = score_answer_llm(query, expected, answer, retrieved)

        # 5. Save to results (с гарантией, что score — первый ключ)
        result = OrderedDict([
            ("score", score),
            ("query", query),
            ("expected", expected),
            ("retrieved_chunks", retrieved),
            ("history", history[-history_len:]),
            ("answer", answer)
        ])
        results.append(result)

        if score <= 0:
            failed.append({
                "query": query,
                "expected_keywords": expected,
                "answer": answer
            })
        else:
            success.append({
                "query": query,
                "expected_keywords": expected,
                "answer": answer
            })

        # 6. Track dialog history
        history.append(f"Q: {query}\nA: {answer}")

    # 7. Save outputs
    with open(output_dir / "answers.jsonl", "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # 8. Save failed and success queries
    if failed:
        with open(output_dir / "failed_queries.jsonl", "w", encoding="utf-8") as f:
            for r in failed:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    if success:
        with open(output_dir / "success_queries.jsonl", "w", encoding="utf-8") as f:
            for r in success:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # 9. Save metrics
    metrics = compute_metrics(results)
    metrics["gen_tokens"] = stats["gen_tokens"]
    metrics["embed_tokens"] = stats["embed_tokens"]
    metrics["llm_calls"] = stats["calls"]

    with open(output_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    with open(output_dir / "config_used.yaml", "w", encoding="utf-8") as f:
        yaml.dump(config, f)

    with open(output_dir / "prompt_used.txt", "w", encoding="utf-8") as f:
        f.write(PROMPT_TEMPLATE)

    print("✅ Evaluation finished")
