import unittest
import sc2reader
from replay.replay import CoOpReplay
from reports.resources.resource_bank import ResourceBankReport

class MyTestCase(unittest.TestCase):
    def test_something(self):
        file_path = "/home/mohammad/StarCraft II/Accounts/1176921989/2-S2-1-11021412/Replays/commanders/nova/abathur/Chain of Ascension-375.SC2Replay"

        replay2 = sc2reader.load_replay(file_path)
        coopReplay = CoOpReplay(replay2)
        players = coopReplay.getPlayers()

        report = ResourceBankReport(file_path)
        report.report(players)
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
