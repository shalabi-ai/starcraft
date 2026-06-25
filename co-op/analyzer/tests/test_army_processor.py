from pathlib import Path

import pytest
import sc2reader

from replay.army_processor import ArmyProcessor

TEST_DATA_DIR = Path(__file__).parent / "commanders"

FILES = [p for p in TEST_DATA_DIR.rglob("*.SC2Replay") if p.is_file()]

ephemerals = set()
COUNTER = 0
FILES_PROBLEM = []
@pytest.mark.parametrize(
    "file_path",
    FILES,
    ids=lambda p: str(p.relative_to(TEST_DATA_DIR)),
)
def test_ephemeral_units(file_path):
    not_ephemerals = ["Roach", "Dragoon", "Scout", "Baneling", "HighTemplar", "HunterKiller", "HunterKiller",
                      "HybridDestroyer", "HybridReaver", "InfestorTerran", "TrooperMengsk", "TrooperMengskImproved",
                      "HellbatBlackOps", "HotSRaptor", "DehakaSwarmHost"]
    global ephemerals
    global COUNTER
    global FILES_PROBLEM
    replay1 = sc2reader.load_replay(str(file_path))
    COUNTER=COUNTER+1
    processor = ArmyProcessor(replay1)
    units, unit_events, resource_events = processor.process_replay()
    ephemeral = processor.ephemeral_units(units)
    if any(item in ephemeral for item in not_ephemerals):
        FILES_PROBLEM.append(str(file_path))
       # print(file_path)
    ephemerals = ephemerals | ephemeral
    print(ephemerals)

def test_problem():
    file_path = "/home/mohammad/learn/starcraft/co-op/analyzer/tests/commanders/raynor/kerrigan/Dead of Night-normal-4.SC2Replay"
    replay1 = sc2reader.load_replay(str(file_path))
    processor = ArmyProcessor(replay1)
    units, unit_events, resource_events = processor.process_replay()
    ephemeral = processor.ephemeral_units(units)
    print(ephemeral)
