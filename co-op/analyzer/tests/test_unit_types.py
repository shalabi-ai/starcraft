from pathlib import Path

import pytest
import sc2reader

from replay.army_processor import ArmyProcessor

TEST_DATA_DIR = Path(__file__).parent / "commanders/tychus/abathur"

FILES = [p for p in TEST_DATA_DIR.rglob("*.SC2Replay") if p.is_file()]

types = set()
types1 = set()
COUNTER = 0
FILES_PROBLEM = []
commander = ""
@pytest.mark.parametrize(
    "file_path",
    FILES,
    ids=lambda p: str(p.relative_to(TEST_DATA_DIR)),
)
def test_unit_types(file_path):
    global commander
    global types
    global types1
    global COUNTER
    global FILES_PROBLEM
    nova = str(file_path).split("tychus/")[1]
    c = nova.split("/")[0]
    if c != commander and commander!="":
        types1 = set()
    commander = c

    replay1 = sc2reader.load_replay(str(file_path))
    COUNTER=COUNTER+1
    processor = ArmyProcessor(replay1)
    units, unit_events, resource_events = processor.process_replay()


    for unit in units.values():
        types.add(unit.current_type)
        types1.add(unit.current_type)

    print(types1)



