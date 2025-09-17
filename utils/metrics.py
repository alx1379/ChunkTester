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
