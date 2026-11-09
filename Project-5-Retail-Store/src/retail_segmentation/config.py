"""Load pipeline settings from configs/config.yaml.

A plain dict loaded from YAML is enough here — the pipeline just reads a
handful of paths and numbers, so a config-object framework would be
over-engineering for the problem size.
"""

from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "config.yaml"


def load_config(path: Path | str = DEFAULT_CONFIG_PATH) -> dict:
    """Read the YAML config file and resolve relative paths to project root."""
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    cfg["data"]["raw_path"] = str(PROJECT_ROOT / cfg["data"]["raw_path"])
    cfg["features"]["processed_path"] = str(PROJECT_ROOT / cfg["features"]["processed_path"])
    cfg["model"]["artifact_path"] = str(PROJECT_ROOT / cfg["model"]["artifact_path"])
    cfg["model"]["labeled_output_path"] = str(PROJECT_ROOT / cfg["model"]["labeled_output_path"])
    cfg["reports"]["figures_dir"] = str(PROJECT_ROOT / cfg["reports"]["figures_dir"])
    cfg["reports"]["k_scores_path"] = str(PROJECT_ROOT / cfg["reports"]["k_scores_path"])
    return cfg
