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


import re
from cleaners.heuristics import INSTRUCTION_PATTERNS

def clean_chunk(text: str) -> str:
    """
    Removes instructions, system phrases, service inserts, and introductory phrases from the text.
    Only used if clean_context_instructions = true.
    """
    cleaned = text

    for pattern in INSTRUCTION_PATTERNS:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

    # Remove multiple spaces and empty lines
    cleaned = re.sub(r"\n{2,}", "\n", cleaned)
    cleaned = re.sub(r"[ \t]{2,}", " ", cleaned).strip()

    return cleaned

def clean_chunks(chunks: list[dict]) -> list[dict]:
    """
    Removes from chunks lines that contain explicit instructions like:
    - 'Answer this question:'
    - 'Question:'
    - 'You are an assistant...'

    Simple filter - can be enhanced with more regex patterns.
    """
    cleaned = []
    for ch in chunks:
        text = ch["chunk"]
        lines = text.splitlines()
        filtered = [
            line for line in lines
            if not any(bad in line.lower() for bad in ["question:", "answer", "you are", "instruction", "assistant:"])
        ]
        ch["chunk"] = "\n".join(filtered).strip()
        cleaned.append(ch)
    return cleaned

