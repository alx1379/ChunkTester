````markdown
# 🧪 RAG ChunkTester

**RAG ChunkTester** is a framework for automated testing of Retrieval-Augmented Generation (RAG) systems.  
It allows you to quickly evaluate the impact of different chunking strategies, embedding configurations, retriever parameters, and prompts.

---

## 📁 Project Structure

chunktester/
├── main.py                    # Entry point: run chunking, eval, sweep, summary
├── runners/                   # Execution modules
│   ├── chunk_and_embed.py
│   ├── eval_runner.py
│   └── sweep_runner.py
├── utils/                     # Utility helpers
│   ├── config_loader.py
│   ├── document_loader.py
│   ├── chunking.py
│   ├── embedding.py
│   ├── retriever.py
│   └── logger.py
├── cleaners/                  # Optional chunk cleaning
│   └── chunk_cleaner.py
├── scorers/
│   └── llm_scorer.py          # Response evaluation (+1 / 0 / -1)
├── prompts/
│   └── system_prompt.txt      # Instruction for LLM
├── configs/
│   ├── eval_config.yaml       # Config for a single run
│   ├── sweep_grid.yaml        # Grid search parameters
│   └── settings.py            # Keys and proxy from .env
├── data/
│   ├── source_docs/           # Documents for chunking
│   └── queries.jsonl          # Queries + expected keywords
├── embeddings/                # ChromaDB storage (one folder per run)
├── results/                   # Evaluation results (one folder per run)
├── .env                       # API keys and options
├── .gitignore
└── requirements.txt

---

## 🚀 Quick Start

1. **Set up dependencies and create a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate # for Unix
.\venv\Scripts\activate.bat # for Windows
pip install -r requirements.txt
````

2. **Configure `.env` with your keys:**

```env
OPENAI_API_KEY=sk-...
USE_PROXY=false
PROXY_URL=http://localhost:8080
OPENAI_MODEL=gpt-4
```

3. **Place documents into `data/source_docs/`** (`.txt`, `.md`, etc.)

4. **Define queries in `data/queries.jsonl`:**

```json
{"query": "Who is Mr. X?", "expected_keywords": ["director", "analytics"]}
```

5. **Make sure `prompts/system_prompt.txt` contains your instruction**

---

## 🧪 Question Generation - positive/negative/hallucination

```bash
python generate_questions.py
```

---

## 🧪 Single Experiment

```bash
python main.py run_chunk --config configs/eval_config.yaml
python generate_questions.py
python main.py run_eval  --config configs/eval_config.yaml
python main.py summary
python main.py show_fails
python main.py run_eval --config configs/eval_config.yaml --queries data/failed_queries.jsonl
```

---

## 🔁 Multiple Experiments (sweep)

```bash
python main.py run_sweep --sweep configs/sweep_zip.yaml
python main.py summary
```

---

## 📊 Evaluation

The scoring metric is based on:

* `+1` — all expected keywords found in the answer
* `0` — some keywords found
* `-1` — no keywords found

Example output:

```text
=== Summary ===
✅ sweep_a1655fdd: acc=0.87, halluc=0.00 | +1=13, 0=1, -1=1
```

---

## ⚠️ Important Notes

* `run_chunk` **always creates a new collection** (unique `run_id`)
* `run_eval` uses the `run_id` corresponding to the current config
* if the config does not change — you can rerun `run_eval` without `run_chunk`

---

## 📌 Planned Improvements

* [ ] Embedding caching by document hash
* [ ] LLM hallucination check (controlled off-context response)
* [ ] Graphical analysis of sweep runs
* [ ] `run_all` wrapper for a full pipeline run

---

## 🤝 Author

This system was developed for internal RAG system testing.
Contact: \[e-mail: [alx1379@gmail.com](mailto:alx1379@gmail.com)]

```
