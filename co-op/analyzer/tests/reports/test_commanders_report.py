import unittest
from replay.analyser_factory import AnalyserFactory
from reports.commanders import Commanders

class MyTestCase(unittest.TestCase):
    def test_something(self):
        path = "/home/mohammad/StarCraft II/Accounts/1176921989/2-S2-1-11021412/Replays/commanders/nova/abathur/Chain of Ascension-375.SC2Replay"
        analyser= AnalyserFactory.create_analyser(path)

        commanders = Commanders(analyser)
        commanders.plot_commanders_chart()

        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
