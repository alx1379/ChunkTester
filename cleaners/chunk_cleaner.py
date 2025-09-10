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

