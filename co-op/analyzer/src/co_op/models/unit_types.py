from models.unit_type.army_unit import ARMY_UNITS
from models.unit_type.buildings_units import BUILDINGS_UNITS, BUILDING_KEYWORDS
from models.unit_type.commander_ability import COMMANDER_ABILITY
from models.unit_type.commander_units import COMMANDER_UNITS
from models.unit_type.temporary_units import TEMPORARY


class UnitTypes:
    def __init__(self, unit_type: str):
        self.type = unit_type.lower()
        self.unit_type = unit_type
    def is_worker(self)->bool:
        workers = {"DroneStetmann", "SCVMengsk", "TychusSCV", "HHSCV", "SISCV"}
        if self.unit_type in workers:
            return True
        return (
                self.type.endswith(("drone", "scv", "probe", "mule"))
                and "egg" not in self.type
        )

    def is_building(self)->bool:
        if self.__is_exist__(BUILDINGS_UNITS):
            return True

        return self.__contains_keyword__(BUILDING_KEYWORDS)

    def is_temporary(self)->bool:
        return self.__is_exist__(TEMPORARY)

    def is_army(self) ->bool:
        if self.__is_exist__(ARMY_UNITS):
            return True

        if self.is_commander():
            return True

        if self.__is_exist__(COMMANDER_UNITS):
            return True

        if self.is_worker():
            return False

        if self.is_building():
            return False

        return True

    def is_commander(self)->bool:
        commander_set = {"NovaCoop", "AlarakCoop", "ZagaraCoop", "K5Kerrigan", "TychusCoop", "DehakaCoop", "GaryStetmann",
                         "DrakkenLaserDrillCoop", "SoACasterKarax", "CoopCasterHorner", "SoACasterVorazun",
                         "CoopCasterStukov", "FenixCoop", "ZeratulCoop"}
        return self.__is_exist__(commander_set)

    def is_commander_unit(self) ->bool:
        return self.__is_exist__(COMMANDER_UNITS)

    def  is_commander_ability(self)->bool:
        return self.__is_exist__(COMMANDER_ABILITY)

    def __contains_keyword__(self, items)->bool:
        return any(
            keyword in self.unit_type
            for keyword in items
        )
    def __is_exist__(self, items)->bool:
        return self.unit_type in items