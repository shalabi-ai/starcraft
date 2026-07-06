import unittest
from replay.replay import CoOpReplay
from replay.army_analyser import ArmyAnalyser
from replay.army_processor import ArmyProcessor
import sc2reader

from tests import TESTS_FILES_PATH


class MyTestCase(unittest.TestCase):
    def test_army_state_timeline(self):
        replay1 = sc2reader.load_replay("/home/mohammad/StarCraft II/Accounts/1176921989/2-S2-1-11021412/Replays/commanders/nova/abathur/Chain of Ascension-375.SC2Replay")

        processor = ArmyProcessor(replay1)
        results = processor.process_replay()
        units = results["all_units"]
        unit_events = results["unit_events"]

        coopReplay = CoOpReplay(replay1)
        players = coopReplay.getPlayerMap()

        analyser = ArmyAnalyser(units, unit_events, players)
        df = analyser.army_state_timeline()
        self.assertEqual(True, True)  # add assertion here

    def test_army_value_timeline(self):
        replay1 = sc2reader.load_replay(TESTS_FILES_PATH)

        processor = ArmyProcessor(replay1)
        results = processor.process_replay()
        units = results["all_units"]
        unit_events = results["unit_events"]

        coopReplay = CoOpReplay(replay1)
        players = coopReplay.getPlayerMap()

        analyser = ArmyAnalyser(units, unit_events, players)
        df = analyser.army_value_timeline()
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
