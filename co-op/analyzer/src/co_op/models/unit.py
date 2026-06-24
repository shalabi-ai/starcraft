from dataclasses import dataclass, field


@dataclass
class Unit:
    unit_id: int
    owner: int

    current_type: str

    commander_ability = False

    is_army: bool
    is_building: bool
    is_worker: bool
    is_temporary = False
    is_commander_unit = False
    is_commander = False


    birth_frame: int
    death_frame: int | None = None

    type_history: list = field(default_factory=list)
