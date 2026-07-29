from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class NationalPark:
    name: str
    state: str
    lat: float
    lon: float


def _load_parks() -> list[NationalPark]:
    config_path = Path(__file__).parent / "parks.yaml"
    with config_path.open() as f:
        data = yaml.safe_load(f)
    return [NationalPark(**entry) for entry in data["parks"]]


NATIONAL_PARKS: list[NationalPark] = _load_parks()
