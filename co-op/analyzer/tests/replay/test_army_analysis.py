import unittest
from replay.replay import CoOpReplay
from replay.army_analyser import ArmyAnalyser
from replay.army_processor import ArmyProcessor
import sc2reader


class MyTestCase(unittest.TestCase):
    def test_something(self):
        replay1 = sc2reader.load_replay("/home/mohammad/StarCraft II/Accounts/1176921989/2-S2-1-11021412/Replays/commanders/nova/abathur/Chain of Ascension-375.SC2Replay")

        processor = ArmyProcessor(replay1)
        units, unit_events = processor.process_replay()

        coopReplay = CoOpReplay(replay1)
        players = coopReplay.getPlayerMap()

        analyser = ArmyAnalyser(unit_events, players)
        df = analyser.army_state_timeline()
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
