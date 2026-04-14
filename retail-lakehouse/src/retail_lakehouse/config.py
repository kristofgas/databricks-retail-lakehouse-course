"""Load environment-specific configuration from YAML files in conf/."""

from pathlib import Path
from typing import Any

import yaml


_CONF_DIR = Path(__file__).resolve().parents[2] / "conf"


def load_config(env: str = "dev") -> dict[str, Any]:
    """Read conf/{env}.yml and return it as a plain dict."""
    config_path = _CONF_DIR / f"{env}.yml"
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path) as f:
        return yaml.safe_load(f)


def get_table_fqn(config: dict[str, Any], table_key: str) -> str:
    """Return the fully-qualified table name: catalog.schema.table."""
    catalog = config["catalog"]
    schema = config["schema"]
    table = config["tables"][table_key]
    return f"{catalog}.{schema}.{table}"
