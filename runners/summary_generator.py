# Copyright 2025 Alex Erofeev / AIGENTTO
# Created by Alex Erofeev at AIGENTTO (http://aigentto.com/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import json

def extract_datetime_from_run_id(run_id: str) -> str:
    """
    Returns the YYYYMMDD_HHMMSS part from run_id if present.
    Example: sweep_abc123_20250601_093810 → 20250601_093810
    """
    parts = run_id.split("_")
    return parts[-2] + "_" + parts[-1] if len(parts) >= 3 else ""

def generate_summary(results_dir="results"):
    rows = []
    total_gen_tokens = 0
    total_embed_tokens = 0
    total_calls = 0

    for run in os.listdir(results_dir):
        path = os.path.join(results_dir, run, "metrics.json")
        if not os.path.isfile(path):
            continue
        with open(path) as f:
            m = json.load(f)

        gen_tokens = m.get("gen_tokens", 0)
        embed_tokens = m.get("embed_tokens", 0)
        llm_calls = m.get("llm_calls", 0)

        total_gen_tokens += gen_tokens
        total_embed_tokens += embed_tokens
        total_calls += llm_calls

        rows.append({
            "run_id": run,
            "acc": m.get("accuracy", 0),
            "halluc": m.get("hallucination_rate", 0),
            "score_1": m.get("score_1", 0),
            "score_0": m.get("score_0", 0),
            "score_-1": m.get("score_-1", 0),
            "gen_tokens": gen_tokens,
            "embed_tokens": embed_tokens,
            "llm_calls": llm_calls,
            "sort_key": extract_datetime_from_run_id(run)
        })

    rows.sort(key=lambda x: x["sort_key"], reverse=True)

    print("\n=== Summary ===\n")
    for row in rows:
        acc_color = "✅" if row["acc"] > 0.85 else ("🟡" if row["acc"] > 0.65 else "🔴")
        print(f"{acc_color} {row['run_id']}: acc={row['acc']:.2f}, halluc={row['halluc']:.2f} | "
              f"+1={row['score_1']}, 0={row['score_0']}, -1={row['score_-1']} | "
              f"gen_tokens={row['gen_tokens']}, embed_tokens={row['embed_tokens']}, calls={row['llm_calls']}")

    print("\n=== Totals ===")
    estimated_cost_usd = total_gen_tokens / 1_000_000 * 2 + total_embed_tokens / 1_000_000 * 0.02
    print(f"📊 Gen tokens: {total_gen_tokens:,}")
    print(f"📊 Embed tokens: {total_embed_tokens:,}")
    print(f"📞 Total LLM calls: {total_calls:,}")
    print(f"💸 Estimated cost: ${estimated_cost_usd:.4f} USD")


if __name__ == "__main__":
    generate_summary()
