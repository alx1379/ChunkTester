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
