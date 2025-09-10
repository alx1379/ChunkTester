import re

# by_words: chunk_size and overlap in number of words
# by_paragraphs: chunk_size in chars, overlap in words
# by_sentences: chunk_size in chars, overlap in words
# raw: chunk_size and overlap in chars
def chunk_text(text: str, strategy: str = "by_words", chunk_size: int = 300, overlap: int = 50) -> list[str]:
    """
    Splits text into chunks according to the specified strategy.
    
    strategy:
        - raw: one large chunk
        - by_paragraphs: by paragraphs
        - by_sentences: by sentences
        - by_words: by word count
    """

    if strategy == "raw":
        chunks = []
        step = max(chunk_size - overlap, 1)
        for i in range(0, len(text), step):
            chunks.append(text[i:i + chunk_size])
        return chunks

    def count_words(s):
        return len(s.split())

    chunks = []

    if strategy == "by_paragraphs":
        parts = [p.strip() for p in text.split("\n") if p.strip()]
    elif strategy == "by_sentences":
        parts = re.split(r'(?<=[.!?])\s+', text.strip())
    elif strategy == "by_words":
        words = text.strip().split()
        step = max(chunk_size - overlap, 1)
        for i in range(0, len(words), step):
            chunk_words = words[i:i + chunk_size]
            chunks.append(" ".join(chunk_words))
        return chunks
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

    # Common logic for by_paragraphs and by_sentences
    buffer = []
    char_count = 0

    for part in parts:
        buffer.append(part)
        char_count += len(part)

        if char_count >= chunk_size:
            chunk = " ".join(buffer)
            chunks.append(chunk)

            # Prepare overlap (by words)
            if overlap > 0:
                # Approximate reverse slicing
                overlap_words = chunk.split()[-overlap:]
                buffer = [" ".join(overlap_words)]
                char_count = count_words(buffer[0])
            else:
                buffer = []
                char_count = 0

    if buffer:
        chunks.append(" ".join(buffer))

    return chunks

def chunk_text_tester():
    test_text = """This is paragraph number 0. This is the first paragraph.
This is the second paragraph, it's longer.
Third sentence. Fourth sentence!
Fifth sentence?
"""

    # Test raw strategy
    print("\n=== raw ===")
    chunks = chunk_text(test_text, "raw")
    print("Chunks:", chunks)
    
    # Test by_paragraphs strategy
    print("\n=== by_paragraphs ===")
    chunks = chunk_text(test_text, "by_paragraphs", chunk_size=50, overlap=2)
    print("Chunks:", chunks)
    
    # Test by_sentences strategy
    print("\n=== by_sentences ===")
    chunks = chunk_text(test_text, "by_sentences", chunk_size=10, overlap=0)
    print("Chunks:", chunks)
    
    # Test by_words strategy
    print("\n=== by_words ===")
    chunks = chunk_text(test_text, "by_words", chunk_size=3, overlap=0)
    print("Chunks:", chunks)

# Run the tester
# chunk_text_tester()
