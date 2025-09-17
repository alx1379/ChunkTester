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


import os
import hashlib
from codenamize import codenamize

from datetime import datetime

import chromadb
from utils.document_loader import load_all_documents
from utils.chunking import chunk_text
from llm.embedding import embed_chunks
from utils.logger import log_step
from cleaners.chunk_cleaner import clean_chunks


def run_chunk_and_embed(config: dict) -> str:
    log_step("🔨 Start chunking and embedding")

    # Unique run_id
#    hash_part = hashlib.sha1(str(config).encode()).hexdigest()[:8]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#    run_id = f"sweep_{hash_part}_{timestamp}"
#    run_id = f"sweep_{codenamize(str(timestamp).encode('utf-8'))}_{timestamp}"
#    output_path = f"embeddings/{run_id}"
#    os.makedirs(output_path, exist_ok=True)

    # Loading and chunking documents
    documents = load_all_documents("data/source_docs/")
    all_chunks = []
    for doc in documents:
        chunks = chunk_text(
            text=doc["text"],
            strategy=config["chunking"]["strategy"],
            chunk_size=config["chunking"]["chunk_size"],
            overlap=config["chunking"]["overlap"]
        )
        for ch in chunks:
            all_chunks.append({
                "chunk": ch,
                "source": doc["name"]
            })

    log_step(f"📄 Total chunks: {len(all_chunks)}")

    run_id = f"sweep_{config["chunking"]["strategy"]}_{config["chunking"]["chunk_size"]}_{config["chunking"]["overlap"]}_{timestamp}"
    output_path = f"embeddings/{run_id}"
    os.makedirs(output_path, exist_ok=True)

    # Clean instructions from chunks (optional)
    if config.get("clean_context_instructions", False):
        all_chunks = clean_chunks(all_chunks)
        log_step("🧹 Cleaned chunks")

    # Getting embeddings
    chunk_texts = [c["chunk"] for c in all_chunks]
    embeddings = embed_chunks(chunk_texts, model=config["embedding"]["model"])

    # Creating ChromaDB collection and loading chunks
    client = chromadb.PersistentClient(path=output_path)
    collection = client.get_or_create_collection("rag_eval")

    for i, chunk in enumerate(all_chunks):
        print(f"\n📄 Chunk {i+1}:\n{chunk}")
        collection.add(
            ids=[f"{run_id}_{i}"],
            documents=[chunk["chunk"]],
            metadatas=[{"source": chunk["source"]}],
            embeddings=[embeddings[i]]
        )


    log_step(f"✅ Embedding finished and saved to {output_path}")

    # Save run_id
    with open(os.path.join("embeddings/", "run_id.txt"), "w", encoding="utf-8") as f:
        f.write(run_id)

    return run_id
