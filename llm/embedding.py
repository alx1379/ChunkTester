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


from llm.generate import openai_client, stats

def embed_chunks(texts: list[str], model: str = "text-embedding-3-small") -> list[list[float]]:
    response = openai_client.embeddings.create(
        model=model,
        input=texts
    )

    if response.usage:
        stats["embed_tokens"] += response.usage.total_tokens
        stats["calls"] += 1

    return [item.embedding for item in response.data]
