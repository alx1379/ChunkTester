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


from llm.generate import generate_llm_answer

def score_answer_llm(query: str, expected: str, actual: str, retrieved_chunks: list[str]) -> int:
    """
    Evaluates the correctness and relevance of the answer considering the retrieved_chunks.
    """
    chunks_text = "\n---\n".join(retrieved_chunks)

    prompt = (
        f"User asked the following question:\n\n{query}\n\n"
        f"Assistant responded with:\n\n{actual}\n\n"
        f"Expected information (keywords that should be in the answer):\n\n{expected}\n\n"
        f"Context provided to the assistant (retrieved_chunks):\n\n{chunks_text}\n\n"
        "Rate the answer on the following scale:\n"
        "- `+1`: The answer contains **all or most** of the key information from the expectations.\n"
        "- `0`: The assistant **did not answer the question**, refused to answer, or went off-topic.\n"
        "- `-1`: The assistant **provided a confident but incorrect answer** that doesn't match the expectations or context.\n\n"
        "**Important:** Do not give +1 if the assistant honestly refused to answer and didn't provide the expected information.\n"
        "Response: Only one of: +1, 0, -1."
    )

    print(">>> SCORER:", prompt)
    raw_result = generate_llm_answer(prompt, model="gpt-4o").strip()
    print(">>> SCORER llm result:", raw_result)

    if "+1" in raw_result:
        return 1
    elif "-1" in raw_result:
        return -1
    else:
        return 0


def score_answer_llm_negative(query: str, actual: str, retrieved_chunks: list[str]) -> int:
    """
    Evaluates the assistant's behavior on a negative (control) question, considering the retrieved_chunks.
    """
    chunks_text = "\n---\n".join(retrieved_chunks)

    prompt = (
        f"User asked the following question:\n\n{query}\n\n"
        f"Assistant responded with:\n\n{actual}\n\n"
        f"Context provided to the assistant:\n\n{chunks_text}\n\n"
        "Analyze the response and rate it strictly on this scale:\n"
        "- `+1`: The assistant **correctly stated that it cannot answer** the question because the context lacks the necessary information.\n"
        "- `0`: The assistant did not provide a clear answer, went off-topic, or responded with overly general phrases.\n"
        "- `-1`: The assistant **confidently answered the question** when it shouldn't have (this is a negative test, and the correct answer should be 'I don't know').\n\n"
        "**Important:** If the assistant couldn't find the answer in the context and honestly admitted it — give +1.\n"
        "Response: Only one of: +1, 0, -1."
    )

    print(">>> NEG SCORER:", prompt)
    raw_result = generate_llm_answer(prompt, model="gpt-4o").strip()
    print(">>> NEG SCORER result:", raw_result)

    if "+1" in raw_result:
        return 1
    elif "-1" in raw_result:
        return -1
    else:
        return 0
