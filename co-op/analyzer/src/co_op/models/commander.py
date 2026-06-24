from dataclasses import dataclass, field

from models.unit import Unit


@dataclass
class Commander:
    unit_id: int
    owner: int
    name: str
    units_ids: set[int] = field(default_factory=set)