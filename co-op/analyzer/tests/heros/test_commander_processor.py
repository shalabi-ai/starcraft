import unittest

import sc2reader

from heros.commander_processor import CommanderProcessor
from tests import TESTS_FILES_PATH


class MyTestCase(unittest.TestCase):
    def test_something(self):
        replay1 = sc2reader.load_replay(TESTS_FILES_PATH)
        processor = CommanderProcessor(replay1)
        units, kills, kill_events, hero_events =  processor.process_replay()

        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
