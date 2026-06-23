import unittest
from replay.replay import CoOpReplay
from replay.army_analyser import ArmyAnalyser
from replay.army_processor import ArmyProcessor
import sc2reader

from tests import TESTS_FILES_PATH


class MyTestCase(unittest.TestCase):
    def test_temporary_units_set(self):
        replay1 = sc2reader.load_replay(TESTS_FILES_PATH)

        processor = ArmyProcessor(replay1)
        units, unit_events = processor.process_replay()

        u = processor.temporary_units(units)
        self.assertEqual(True, True)  # add assertion here



if __name__ == '__main__':
    unittest.main()
