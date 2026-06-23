from collections import defaultdict
from sc2reader.resources import Replay

from heros.heros import is_hero
from models.unit import Unit
from replay import FRAME_RATE

HEROS = {
    "Dehaka",
    "Tychus"
}

COMMANDER_POWER_UNITS = {
    "TychusCoop",
    "TychusWarhound",
    "TychusMedic",
    "TychusHERC",
    "TychusFirebat",

    "DehakaCoop",
    "DehakaCoopClone",
    "DehakaMurvar",
    "DehakaDakrun",
    "DehakaGlevig",

    #aba
    "Brutalisk",
    "Leviathan",
}

POWER_VALUES = {
    "DehakaCoop": 1000,
    "DehakaCoopClone": 300,
    "DehakaMurvar": 800,
    "DehakaDakrun": 800,
    "DehakaGlevig": 800,

    "TychusCoop": 1000,
    "TychusWarhound": 800,
    "TychusMedic": 700,
    "TychusHERC": 700,
    "TychusFirebat": 800,
}

HERO_IGNOR = [
    "DehakaTrainEggRoach",
    "DehakaTrainEggDrone",
    "DehakaDrone",
    "DehakaHatchery",
    "DehakaCoopReviveCocoonFootPrint",
    "DehakaTrainEggHydralisk",
    "TychusSCV",
    "TychusCommandCenter",
    "TychusResearchCenter",
    "TychusWarhoundAutoTurret",
    "TychusResearchCenterUnlocked",
    "TychusResearchCenterLocked",
    "SupplyDepotLowered",
    "Egg",
    "SiegeTankSieged",
    "Larva",
    "ToxicNestBurrowed",

    #"BiomassPickup",
]
DEHAKA = {
    "DehakaTrainEggRoach",
    "DehakaTrainEggDrone",
    "DehakaDrone",
    "DehakaCreeperFlying",
}
TYCHUS_OUTLAWS = {
    "TychusMedic",
    "TychusSCV",
    "TychusWarhoundAutoTurret",
    "TychusResearchCenterUnlocked",
    "TychusResearchCenterLocked",
    "TychusHERC",
    "TychusOdin",
    "TychusCommandCenter",
    "TychusResearchCenter"
    "CoopCasterTychus"
    "TychusCoop",
    "TychusWarhound",
    "TychusFirebat",
    "TychusHERC"
    "Tychus",
    "Sirius",
    "Nux",
    "Sam",
    "Blaze",
    "Rattlesnake",
    "Vega",
    "Cannonball"
}
class CommanderProcessor:
    def __init__(self, replay: Replay, players_ids=None):
        if players_ids is None:
            players_ids = [1, 2]
        self.players_ids = set(players_ids)
        self.replay = replay

    def process_replay(self):
        ignor_set = set(HERO_IGNOR)
        units = {}
        kills = defaultdict(lambda: defaultdict(int))
        hero_events = []
        kill_events = []

        replay = self.replay

        event_types = {"UnitBornEvent", "UnitTypeChangeEvent", "UnitTypeChangeEvent"}
        for event in replay.tracker_events:
            if not event.name in event_types:
                continue
            if event.unit_type_name in ignor_set:
                continue
            unit = event.unit
            if unit.is_building or unit.is_worker:
                continue

            owner = getattr(event, "control_pid", None)
            if owner is None or owner == 0 or not owner in self.players_ids:
                continue

            # -------------------------
            # Unit is created
            # -------------------------
            if event.name == "UnitBornEvent":


                units[event.unit_id] = {
                    "type": event.unit_type_name,
                    "owner": event.control_pid
                }

                # Hero tracking
                has_hero, hero = is_hero(event.unit_type_name)
                if has_hero:
                    hero_events.append({
                        "time_sec": int(event.second),
                        "frame": event.frame,
                        "player_id": event.control_pid,
                        "hero_name": event.unit_type_name,
                        "event_type": (
                            "spawn"
                            if event.unit_type_name == "Tychus"
                            else "hire"
                        ),
                        "unit_id": event.unit_id
                    })

            elif event.name == "UnitTypeChangeEvent":
                hero_events.append({
                    "event_type": "evolution",
                    "frame": event.frame,
                    "time_sec": int(event.frame / FRAME_RATE),
                    "hero_name": event.unit_type_name,
                    "unit_id": event.unit_id
                })

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

        return units, kills, kill_events, hero_events