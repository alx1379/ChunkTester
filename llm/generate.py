import openai
import httpx

from configs.settings import (
    OPENAI_API_KEY,
    USE_PROXY,
    PROXY_URL
)

# Статистика по использованию LLM
stats = {
    "gen_tokens": 0,
    "embed_tokens": 0,
    "calls": 0
}

# Настраиваем OpenAI-клиент с прокси (если указано)
if USE_PROXY and PROXY_URL:
    transport = httpx.HTTPTransport(proxy=PROXY_URL, verify=False)
    http_client = httpx.Client(transport=transport)
    openai_client = openai.OpenAI(api_key=OPENAI_API_KEY, http_client=http_client)
else:
    openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)


def generate_llm_answer(prompt: str, model: str = "gpt-4o-mini") -> str:
    response = openai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": (
                "Ты — строго функциональный помощник. Отвечай исключительно по предоставленному контексту. "
                "Не проявляй инициативу, не выражай заботу и не предлагай помощь. "
                "Не добавляй вежливых фраз в конце ответа (например, 'Если у вас есть вопросы...'). "
                "Ответ должен быть точным, кратким и строго по делу, как в технической документации."
            )},        
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )

    if response.usage:
        stats["gen_tokens"] += response.usage.total_tokens
        stats["calls"] += 1

    return response.choices[0].message.content.strip()


def call_llm(prompt: str, model: str = "gpt-4o-mini") -> str:
    response = openai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )

    if response.usage:
        stats["gen_tokens"] += response.usage.total_tokens
        stats["calls"] += 1

    return response.choices[0].message.content.strip()
