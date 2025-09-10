from llm.generate import generate_llm_answer

def score_answer_llm(query: str, expected: str, actual: str, retrieved_chunks: list[str]) -> int:
    """
    Оценивает корректность и релевантность ответа с учётом retrieved_chunks.
    """
    chunks_text = "\n---\n".join(retrieved_chunks)

    prompt = (
        f"Пользователь задал вопрос:\n\n{query}\n\n"
        f"Ассистент ответил:\n\n{actual}\n\n"
        f"Ожидаемая информация (ключевые слова, которые должны быть в ответе):\n\n{expected}\n\n"
        f"Контекст, предоставленный ассистенту (retrieved_chunks):\n\n{chunks_text}\n\n"
        "Оцени ответ по шкале:\n"
        "- `+1`: Ответ содержит **все или большую часть** ключевой информации из ожиданий.\n"
        "- `0`: Ассистент **не ответил на вопрос**, отказался отвечать или ушёл от темы.\n"
        "- `-1`: Ассистент **дал уверенный, но неверный ответ**, не соответствующий ожиданиям или контексту.\n\n"
        "**Важно:** Не ставь +1, если ассистент честно отказался от ответа, и не привёл ожидаемой информации.\n"
        "Ответ: Только одно из: +1, 0, -1."
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
    Оценивает поведение ассистента на негативный (контрольный) вопрос, с учётом retrieved_chunks.
    """
    chunks_text = "\n---\n".join(retrieved_chunks)

    prompt = (
        f"Пользователь задал вопрос:\n\n{query}\n\n"
        f"Ассистент ответил:\n\n{actual}\n\n"
        f"Контекст, предоставленный ассистенту:\n\n{chunks_text}\n\n"
        "Проанализируй ответ и оцени строго по этой шкале:\n"
        "- `+1`: Ассистент честно указал, что не знает или информации нет.\n"
        "- `0`: Ассистент дал нерелевантный, общий или бессмысленный ответ.\n"
        "- `-1`: Ассистент уверенно выдумал информацию, которой нет в контексте.\n\n"
        "Ответ: Только одно из: +1, 0, -1."
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
