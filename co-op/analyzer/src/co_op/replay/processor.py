from collections import defaultdict
from sc2reader.resources import Replay

class ReplayProcessor:
    def __init__(self, replay: Replay):
        self.replay = replay

    def process_replay(self):
        units = {}
        kills = defaultdict(lambda: defaultdict(int))
        kill_events = []

        replay = self.replay
        for event in replay.tracker_events:

            # -------------------------
            # Unit is created
            # -------------------------
            if event.name == "UnitBornEvent":
                value = getattr(event, "control_pid", None)
                if value == None or event.control_pid == 0:
                    continue
                units[event.unit_id] = {
                    "type": event.unit_type_name,
                    "owner": event.control_pid
                }

            # -------------------------
            # Unit dies
            # -------------------------
            elif event.name == "UnitDiedEvent":

                killer_id = getattr(event, "killing_unit_id", None)
                if killer_id == None:
                    continue
                victim_tag = event.unit_id
                killer_tag = killer_id

                victim = units.get(victim_tag)
                killer = units.get(killer_tag)

                if not victim or not killer:
                    continue

                killer_owner = killer["owner"]
                killer_type = killer["type"]

                kills[killer_owner][killer_type] += 1

                kill_events.append({
                    "time": event.frame,
                    "killer_player": killer["owner"],
                    "killer_unit": killer["type"],
                    "victim_player": victim["owner"],
                    "victim_unit": victim["type"]
                })

                # cleanup
                units.pop(victim_tag, None)

        return kills, kill_events


    def print_kills(self, kills):
        for player_id, unit_map in kills.items():
            print(f"\nPlayer {player_id}")

            for unit_type, count in sorted(unit_map.items(), key=lambda x: -x[1]):
                print(f"  {unit_type}: {count}")