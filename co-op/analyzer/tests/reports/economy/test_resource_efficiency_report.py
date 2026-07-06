import unittest

import sc2reader

from replay.army_processor import ArmyProcessor
from reports.resources.resource_efficiency_report import ResourceEfficiencyReport
from tests import TESTS_FILES_PATH


class MyTestCase(unittest.TestCase):
    def test_something(self):
        replay1 = sc2reader.load_replay(TESTS_FILES_PATH)

        processor = ArmyProcessor(replay1)
        results = processor.process_replay()
        resource_events = results["resource_events"]

        report = ResourceEfficiencyReport(resource_events)
        report.plot_resource_efficiency()
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
