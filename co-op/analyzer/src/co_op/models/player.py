from dataclasses import dataclass

from sc2reader.events import Event


@dataclass
class Player:
    id: int
    name: str
    commander: str
    race: str
    events: list[Event]

