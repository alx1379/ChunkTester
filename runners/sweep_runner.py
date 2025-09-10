import os
import yaml
from runners.chunk_and_embed import run_chunk_and_embed
from runners.eval_runner import run_eval
from utils.config_loader import generate_sweep_configs

def run_sweep(sweep_path: str):
    with open(sweep_path) as f:
        sweep_raw = yaml.safe_load(f)

    configs = generate_sweep_configs(sweep_raw)
    print(f"🔁 Running {len(configs)} sweep configurations...\n")

    for i, cfg in enumerate(configs):
        print(f"--- [{i+1}/{len(configs)}] ---")
        run_id = run_chunk_and_embed(cfg)
        run_eval(cfg, run_id=run_id)
