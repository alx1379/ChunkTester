
```markdown
# 🧪 RAG ChunkTester

**RAG ChunkTester** — это фреймворк для автоматического тестирования качества Retrieval-Augmented Generation систем. Он позволяет быстро оценивать влияние разных стратегий чанкования, настройки эмбеддинга, параметров ретривера и промпта.

---

## 📁 Структура проекта

```

chunktester/
├── main.py                    # Точка входа: запуск chunking, eval, sweep, summary
├── runners/                  # Исполняющие модули
│   ├── chunk\_and\_embed.py
│   ├── eval\_runner.py
│   └── sweep\_runner.py
├── utils/                    # Вспомогательные утилиты
│   ├── config\_loader.py
│   ├── document\_loader.py
│   ├── chunking.py
│   ├── embedding.py
│   ├── retriever.py
│   └── logger.py
├── cleaners/                 # Опциональная очистка чанков
│   └── chunk\_cleaner.py
├── scorers/
│   └── llm\_scorer.py         # Оценка ответа (+1 / 0 / -1)
├── prompts/
│   └── system\_prompt.txt     # Инструкция для LLM
├── configs/
│   ├── eval\_config.yaml      # Конфиг для одного прогона
│   ├── sweep\_grid.yaml       # Grid-перебор параметров
│   └── settings.py           # Ключи и прокси из .env
├── data/
│   ├── source\_docs/          # Документы для чанкования
│   └── queries.jsonl         # Вопросы + ожидаемые ключевые слова
├── embeddings/               # Хранилище ChromaDB (одна папка на каждый запуск)
├── results/                  # Результаты оценок (одна папка на запуск)
├── .env                      # API ключи и опции
├── .gitignore
└── requirements.txt

````

---

## 🚀 Быстрый старт

1. **Установи зависимости и создай виртуальное окружение:**

```bash
python -m venv venv
source venv/bin/activate # for Unix
.\venv\Scripts\activate.bat # for windows
pip install -r requirements.txt
````

2. **Настрой `.env` с ключами:**

```env
OPENAI_API_KEY=sk-...
USE_PROXY=false
PROXY_URL=http://localhost:8080
OPENAI_MODEL=gpt-4
```

3. **Положи документы в `data/source_docs/`** (`.txt`, `.md`, и т.д.)

4. **Определи запросы в `data/queries.jsonl`:**

```json
{"query": "Кто такой Мистер Икс?", "expected_keywords": ["директор", "аналитики"]}
```

5. **Убедись, что есть `prompts/system_prompt.txt` с инструкцией**

---

## 🧪 Генерация вопросов - positive/nagative/hallucination

```bash
python generate_questions.py
```bash

---

## 🧪 Один эксперимент

```bash
python main.py run_chunk --config configs/eval_config.yaml
python generate_questions.py
python main.py run_eval  --config configs/eval_config.yaml
python main.py summary
python main.py show_fails
python main.py run_eval --config configs/eval_config.yaml --queries data/failed_queries.jsonl
```

---

## 🔁 Много экспериментов (sweep)

```bash
python main.py run_sweep --sweep configs/sweep_zip.yaml
python main.py summary
```

---

## 📊 Оценка

Метрика основана на:

* `+1` — все ключевые слова найдены в ответе
* `0` — найдена часть ключевых слов
* `-1` — ни одно ключевое слово не найдено

Выводится:

```text
=== Summary ===
✅ sweep_a1655fdd: acc=0.87, halluc=0.00 | +1=13, 0=1, -1=1
```

---

## ⚠️ Важные замечания

* `run_chunk` **всегда создаёт новую коллекцию** (уникальный `run_id`)
* `run_eval` использует тот `run_id`, который соответствует текущему конфику
* если конфигурация не меняется — можно повторно запускать `run_eval` без `run_chunk`

---

## 📌 Планируемые улучшения

* [ ] Кеширование эмбеддингов по hash документов
* [ ] LLM-проверка «галлюцинаций» (контролируемый off-context response)
* [ ] Графический анализ sweep-прогонов
* [ ] Обёртка `run_all` для одного полного запуска

---

## 🤝 Автор

Система разработана для внутреннего тестирования RAG-систем.
Вопросы: [e-mail:alx1379@gmail.com]

```

---
```
