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


# runners/show.py

import json
from pathlib import Path

def show_fails(run_id: str = None):
    print("📉 Showing failed responses (score ≤ 0)")

    if run_id is None:
        try:
            with open("embeddings/run_id.txt", "r", encoding="utf-8") as f:
                run_id = f.read().strip()
        except FileNotFoundError:
            raise ValueError("❌ run_id not provided and embeddings/run_id.txt file not found")

    file_path = Path(f"results/{run_id}/answers.jsonl")
    if not file_path.exists():
        raise FileNotFoundError(f"❌ File with results not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        bad_results = [
            json.loads(line) for line in f
            if line.strip() and json.loads(line)["score"] <= 0
        ]

    print(f"🔍 Found bad responses: {len(bad_results)}\n")

    for r in bad_results:
        print("❓", r["query"])
        print("🧠", r["answer"])
        print("📌", f"score = {r['score']}")
        print("📚 chunks:", r["retrieved_chunks"][:5], "...\n")  # Can be expanded
