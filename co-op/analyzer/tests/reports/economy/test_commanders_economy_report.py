import unittest
import sc2reader
from replay.replay import CoOpReplay
from reports.resources.commanders_economy import CommandersEconomyReport
from replay.replay_factory import ReplayFactory
from tests import TESTS_FILES_PATH


class MyTestCase(unittest.TestCase):
    def test_commanders_report(self):
        #file_path = "/home/mohammad/StarCraft II/Accounts/1176921989/2-S2-1-11021412/Replays/commanders/nova/abathur/Chain of Ascension-375.SC2Replay"
        #file_path = "/home/mohammad/StarCraft II/Accounts/1176921989/2-S2-1-11021412/Replays/commanders/tychus/abathur/Scythe of Amon/Scythe of Amon-237-zerq-ground.SC2Replay"
        #file_path ="/home/mohammad/StarCraft II/Accounts/1176921989/2-S2-1-11021412/Replays/commanders/tychus/abathur/Scythe of Amon/Scythe of Amon-hard-393.SC2Replay"

        file_path = TESTS_FILES_PATH
        replay2 = sc2reader.load_replay(file_path)
        coopReplay = CoOpReplay(replay2)
        players = coopReplay.getPlayers()

        tracker_events = ReplayFactory.replay_from_s2protocol(file_path)
        report = CommandersEconomyReport(tracker_events)
        report.generate_report(players)
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
