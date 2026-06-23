import unittest
from replay.analyser_factory import AnalyserFactory
from reports.commanders import Commanders
from tests import TESTS_FILES_PATH


class MyTestCase(unittest.TestCase):
    def test_something(self):
        #path = "/home/mohammad/StarCraft II/Accounts/1176921989/2-S2-1-11021412/Replays/commanders/nova/abathur/Chain of Ascension-375.SC2Replay"
        path = "/home/mohammad/StarCraft II/Accounts/1176921989/2-S2-1-11021412/Replays/commanders/tychus/abathur/Scythe of Amon/Scythe of Amon-237-zerq-ground.SC2Replay"
        path = TESTS_FILES_PATH
        analyser= AnalyserFactory.create_analyser(path)

        commanders = Commanders(analyser)
        commanders.plot_commanders_chart()

        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
