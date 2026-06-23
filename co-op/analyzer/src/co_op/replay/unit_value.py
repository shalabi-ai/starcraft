from collections import defaultdict

from models.unit_cost import UNIT_COSTS


class UnitValue:
    def __init__(self):
        units = defaultdict(str)
        for unit in UNIT_COSTS:
            if unit.supply == 0:
                continue
            units[unit.unit_type] = unit.minerals + unit.gas

        self.units = units
    def get(self, unit_type: str)->int:
        return self.units.get(unit_type,0)