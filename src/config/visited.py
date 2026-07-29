from pathlib import Path

import yaml


def _load_visited(filename: str) -> frozenset[str]:
    config_path = Path(__file__).parent / filename
    with config_path.open() as f:
        data = yaml.safe_load(f)
    return frozenset(data["visited"])


MALHAR_VISITED: frozenset[str] = _load_visited("malhar_visited.yaml")
