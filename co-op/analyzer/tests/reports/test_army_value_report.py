import unittest
from replay.replay import CoOpReplay
from replay.army_analyser import ArmyAnalyser
from replay.army_processor import ArmyProcessor
import sc2reader
from reports.army_value_report import ArmyValueReport
from tests import TESTS_FILES_PATH


class MyTestCase(unittest.TestCase):
    def test_army_value_report(self):
        #path = "/home/mohammad/StarCraft II/Accounts/1176921989/2-S2-1-11021412/Replays/commanders/nova/abathur/Chain of Ascension-375.SC2Replay"
        #path = "/home/mohammad/StarCraft II/Accounts/1176921989/2-S2-1-11021412/Replays/commanders/tychus/abathur/Scythe of Amon/Scythe of Amon-237-zerq-ground.SC2Replay"
        path = TESTS_FILES_PATH

        replay1 = sc2reader.load_replay(path)

        processor = ArmyProcessor(replay1)
        results = processor.process_replay()
        army_value_timeline = results["army_value_timeline"]

        coopReplay = CoOpReplay(replay1)
        players = coopReplay.getPlayerMap()


        report = ArmyValueReport()
        report.plot_army_value_timeline(army_value_timeline, players)

        self.test_army_value_report1()

        self.assertEqual(True, True)  # add assertion here

    def test_army_value_report1(self):
        #path = "/home/mohammad/StarCraft II/Accounts/1176921989/2-S2-1-11021412/Replays/commanders/nova/abathur/Chain of Ascension-375.SC2Replay"
        #path = "/home/mohammad/StarCraft II/Accounts/1176921989/2-S2-1-11021412/Replays/commanders/tychus/abathur/Scythe of Amon/Scythe of Amon-237-zerq-ground.SC2Replay"
        path = TESTS_FILES_PATH

        replay1 = sc2reader.load_replay(path)

        processor = ArmyProcessor(replay1)
        results = processor.process_replay()
        units = results["all_units"]
        unit_events = results["unit_events"]

        coopReplay = CoOpReplay(replay1)
        players = coopReplay.getPlayerMap()

        analyser = ArmyAnalyser(units, unit_events, players)
        df = analyser.army_value_timeline()

        report = ArmyValueReport()
        report.plot_army_value_timeline1(df)

        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
