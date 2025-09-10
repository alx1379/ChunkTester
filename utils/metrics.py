def compute_metrics(answers: list[dict]) -> dict:
    score_1 = sum(1 for a in answers if a.get("score") == 1)
    score_0 = sum(1 for a in answers if a.get("score") == 0)
    score_m1 = sum(1 for a in answers if a.get("score") == -1)
    total = score_1 + score_0 + score_m1

    return {
        "total_queries": total,
        "score_1": score_1,
        "score_0": score_0,
        "score_-1": score_m1,
        "accuracy": round(score_1 / total, 3) if total else 0.0,
        "hallucination_rate": round(score_m1 / total, 3) if total else 0.0
    }
