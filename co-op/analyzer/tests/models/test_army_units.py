import unittest

from sc2reader.data import UnitType

from models.unit import Unit
from models.unit_type.race_army_unit import RACE_ARMY_UNITS
from models.unit_types import UnitTypes

'''
Army units should not be temporary commander units, commander ability, or commander unit.
'''
class ArmyUnitsTestCase(unittest.TestCase):
    def test_army_units(self):
        for unit_type in RACE_ARMY_UNITS:
            unit = Unit(
                unit_id=1,
                owner=1,
                current_type=unit_type,
                birth_frame= 5
            )
            unit.current_type = unit_type
            unit_types = UnitTypes(unit_type)
            unit_types.set_unit(unit)
            self.assertEqual(False, unit.is_temporary, f'{unit_type} should is temporary commander unit')  # add assertion here


if __name__ == '__main__':
    unittest.main()
