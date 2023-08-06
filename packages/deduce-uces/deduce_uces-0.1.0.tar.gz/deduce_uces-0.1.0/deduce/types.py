from dataclasses import dataclass
from typing import NamedTuple, List, Union


@dataclass
class MinimalUCE:
    id: str
    start: int
    end: int
    percent_identity: float = 100


class UCESet(NamedTuple):
    genome: str
    uces: List[MinimalUCE]
