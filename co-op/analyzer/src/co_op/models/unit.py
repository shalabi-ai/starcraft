from dataclasses import dataclass, field


@dataclass
class Unit:
    unit_id: int
    owner: int

    current_type: str

    # TODO: refact to is_commander_ability
    commander_ability = False

    is_army = False
    is_building = False
    is_worker = False
    is_temporary = False
    is_commander_unit = False
    is_commander = False


    birth_frame: int
    death_frame: int | None = None

    type_history: list = field(default_factory=list)
