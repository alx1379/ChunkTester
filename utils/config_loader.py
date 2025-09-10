import yaml
from itertools import product, zip_longest
import hashlib

def generate_sweep_configs(sweep_data: dict) -> list[dict]:
    fixed = sweep_data.get("fixed", {})
    sweep = sweep_data["sweep"]
    sweep_mode = sweep_data.get("sweep_mode", "grid").lower()

    keys, values = zip(*sweep.items())

    if sweep_mode == "grid":
        combos = product(*values)
    elif sweep_mode == "zip":
        if not all(len(v) == len(values[0]) for v in values):
            raise ValueError("In 'zip' mode all sweep values must have same length")
        combos = zip(*values)
    else:
        raise ValueError(f"Unknown sweep_mode: {sweep_mode}")

    configs = []
    for combo in combos:
        cfg = yaml.safe_load(yaml.dump(fixed))  # deep copy
        for k, v in zip(keys, combo):
            levels = k.split(".")
            d = cfg
            for part in levels[:-1]:
                d = d.setdefault(part, {})
            d[levels[-1]] = v
        configs.append(cfg)

    return configs

def get_run_id_from_config(config: dict) -> str:
    config_str = yaml.dump(config, sort_keys=True)
    hash_id = hashlib.md5(config_str.encode("utf-8")).hexdigest()[:6]
    return f"sweep_{config_str}"
