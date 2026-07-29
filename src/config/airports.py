from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class Airport:
    name: str
    code: str
    state: str
    lat: float
    lon: float


def _load_airports() -> list[Airport]:
    config_path = Path(__file__).parent / "airports.yaml"
    with config_path.open() as f:
        data = yaml.safe_load(f)
    return [Airport(**entry) for entry in data["airports"]]


MAJOR_AIRPORTS: list[Airport] = _load_airports()
