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


import argparse
import os
import json
from runners.chunk_and_embed import run_chunk_and_embed
from runners.eval_runner import run_eval
from runners.sweep_runner import run_sweep
from runners.summary_generator import generate_summary
from runners.show import show_fails 

def load_config(path):
    import yaml
    with open(path, "r") as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description="RAG Eval Framework")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # run_chunk
    chunk_parser = subparsers.add_parser("run_chunk")
    chunk_parser.add_argument("--config", required=True, help="Path to eval_config.yaml")

    # run_eval
    eval_parser = subparsers.add_parser("run_eval")
    eval_parser.add_argument("--config", required=True, help="Path to eval_config.yaml")
    eval_parser.add_argument("--queries", default="data/queries.jsonl", help="Path to queries.jsonl")

    # run_sweep
    sweep_parser = subparsers.add_parser("run_sweep")
    sweep_parser.add_argument("--sweep", required=True, help="Path to sweep.yaml")

    # show_fails
    show_parser = subparsers.add_parser("show_fails")
    show_parser.add_argument("--run_id", required=False, help="Run ID (if not specified, taken from embeddings/run_id.txt)")

    # generate_summary
    summary_parser = subparsers.add_parser("summary")

    args = parser.parse_args()

    if args.command == "run_chunk":
        config = load_config(args.config)
        run_chunk_and_embed(config)

    elif args.command == "run_eval":
        config = load_config(args.config)
        run_eval(config, query_file=args.queries)

    elif args.command == "run_sweep":
        run_sweep(args.sweep)

    elif args.command == "summary":
        generate_summary()

    elif args.command == "show_fails":
        show_fails(args.run_id)

if __name__ == "__main__":
    main()
