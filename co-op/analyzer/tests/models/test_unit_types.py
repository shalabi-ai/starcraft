import unittest

from models.unit_types import UnitTypes


class MyTestCase(unittest.TestCase):
    def test_is_building(self):
        BUILDINGS = {
            # Terran
            "CommandCenter",
            "Barracks",
            "BarracksTechLab",
            "Factory",
            "FactoryTechLab",
            "Starport",
            "StarportTechLab",
            "EngineeringBay",
            "Armory",
            "GhostAcademyNova",

            # Protoss
            "Nexus",
            "Pylon",
            "Forge",
            "CyberneticsCore",
            "WarpGate",
            "RoboticsFacility",
            "TwilightCouncil",
            "TemplarArchive",
            "PhotonCannon",
            "Assimilator",
        }

        for building in BUILDINGS:
            unit_types = UnitTypes(building)
            self.assertEqual(True, unit_types.is_building())  # add assertion here

    def test_is_worker(self):
        valid_worker = {"DehakaDrone", "TychusSCV", "HealingDrone"}

        for worker  in valid_worker:
            unit_types = UnitTypes(worker)
            self.assertEqual(True, unit_types.is_worker())

    def test_invalid_worker(self):
        invalid_worker = {"DehakaTrainEggDrone"}

        for worker  in invalid_worker:
            unit_types = UnitTypes(worker)
            self.assertEqual(False, unit_types.is_worker())

if __name__ == '__main__':
    unittest.main()
