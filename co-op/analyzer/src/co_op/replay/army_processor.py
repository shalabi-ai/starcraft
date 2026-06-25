import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame
from sc2reader.resources import Replay
from models.unit import Unit
from models.unit_types import UnitTypes
from replay import FRAME_RATE
from replay.replay import CoOpReplay

class ArmyProcessor:
    IGNORE_MORPHS = {
        ("Larva", "Egg"),
        ("Egg", "Larva"),

        ("RoachVile", "RavagerVileAbathurCocoon"),
        ("RavagerVileAbathurCocoon", "RoachVile"),

        ("CreepTumorBurrowed", "CreepTumorUsed"),
    }

    def is_cosmetic_morph(self, old_type, new_type):
        if old_type == new_type:
            return True

        if (
                old_type.replace("Burrowed", "")
                ==
                new_type.replace("Burrowed", "")
        ):
            return True

        return (old_type, new_type) in self.IGNORE_MORPHS

    def __init__(self, replay: Replay):
        self.replay = replay

    def frame_to_seconds(self, frame):
        return frame / FRAME_RATE

    def process_replay(self):

        coopReplay = CoOpReplay(self.replay)
        players = coopReplay.getPlayerMap()
        all_units = {}
        unit_events = []

        olg_mineral = 0
        old_gas = 0
        current_mineral = 0
        current_gas = 0
        resource_events = []
        for event in self.replay.tracker_events:
            seconds = self.frame_to_seconds(event.frame)

            # -------------------------
            # Unit Created
            # -------------------------
            if event.name in (
                    "UnitBornEvent",
                    "UnitInitEvent"
            ):

                owner = getattr(event, "control_pid", None)

                if owner is None or owner == 0 or not owner in players:
                    continue

                unit = Unit(
                    unit_id=event.unit_id,
                    owner=owner,
                    current_type=event.unit_type_name,
                    birth_frame= seconds,
                    #is_army=event.unit.is_army,
                    #is_building=event.unit.is_building,
                    #is_worker=event.unit.is_worker,
                )
                unit_types = UnitTypes(event.unit_type_name)
                unit_types.set_unit(unit)

                unit.type_history.append(
                    (event.frame, event.unit_type_name)
                )

                all_units[event.unit_id] = unit

                unit_events.append({
                    "frame": event.frame,
                    "time": seconds,
                    "action": "born",
                    "unit_id": event.unit_id,
                    "unit_type": event.unit_type_name,
                    "player": owner
                })

            #-------------------------
            # PlayerStatsEvent
            #-------------------------
            elif event.name == "PlayerStatsEvent":
                old_gas = current_gas
                old_mineral = current_mineral
                current_gas = event.vespene_current
                current_mineral = event.minerals_current
                resource_events.append({
                    "frame": event.frame,
                    "time": event.second,
                    "player_id": event.pid,
                    "mineral_current": event.minerals_current,
                    "gas_current": event.vespene_current,
                    "gas_collection_rate": event.vespene_collection_rate,
                    "minerals_used_current_army": event.minerals_used_current_army, #Minerals invested in completed army units currently alive
                    "gas_used_current_army": event.vespene_used_current_army,
                    "minerals_lost_army": event.minerals_lost_army, # Minerals invested in army units that have been destroyed
                    "gas_lost_army": event.vespene_lost_army,
                    "minerals_used_current_economy": event.minerals_used_current_economy, # Completed economic assets currently alive for structuers, and worker units.
                    "gas_used_current_economy": event.vespene_used_current_economy,
                    "minerals_lost_economy": event.minerals_lost_economy, # Mineral value of dead workers/economic structures.
                    "gas_lost_economy": event.vespene_lost_economy,
                    "minerals_lost_technology": event.minerals_lost_technology, # The mineral value of technology-producing or technology-enabling structures that have been destroyed. Examples: Barracks Tech Lab, Factory Tech Lab, Starport Tech Lab, Engineering Bay, Armory, Ghost Academy, Fusion Core
                    "gas_lost_technology": event.vespene_lost_technology,

                    # Income Graph
                    "minerals_collection_rate": event.minerals_collection_rate, # per minute
                    "vespene_collection_rate": event.vespene_collection_rate,

                    # army value
                    #"army_count": event.army_count,
                    #"army_value": event.army_value,

                   # "economy_value": event.economy_value,
                   # "technology_value": event.technology_value,
                   # "workers_active_count": event.workers_active_count,

                    # Resource Efficiency
                    "minerals_killed": event.minerals_killed,
                    "vespene_killed": event.vespene_killed,
                    "minerals_lost": event.minerals_lost,  # Resource Losses
                    "vespene_lost": event.vespene_lost,  # Resource Losses
                })

            # -------------------------
            # Unit Morph
            # -------------------------
            elif event.name == "UnitTypeChangeEvent":
                unit = all_units.get(event.unit_id)

                if not unit:
                    continue

                old_type = unit.current_type
                new_type = event.unit_type_name

                unit.current_type = new_type
                unit.type_history.append(
                    (event.frame, event.unit_type_name)
                )

                if not self.is_cosmetic_morph(old_type, new_type):
                    unit_events.append({
                        "frame": event.frame,
                        "time": seconds,
                        "action": "morph",
                        "unit_id": event.unit_id,
                        "player": unit.owner,
                        "old_type": old_type,
                        "new_type": new_type
                    })

            # -------------------------
            # Unit Died
            # -------------------------
            elif event.name == "UnitDiedEvent":

                unit = all_units.get(event.unit_id)

                if not unit:
                    continue

                unit.death_frame = seconds

                unit_events.append({
                    "frame": event.frame,
                    "time": seconds,
                    "action": "died",
                    "unit_id": event.unit_id,
                    "unit_type": unit.current_type,
                    "player": unit.owner
                })

            elif event.name == "UnitDoneEvent":

                unit = all_units.get(event.unit_id)

                if not unit:
                    continue

                unit_events.append({
                    "frame": event.frame,
                    "time": seconds,
                    "action": "complete",
                    "unit_id": unit.unit_id,
                    "player": unit.owner,
                    "unit_type": unit.current_type
                })

        unit_events.sort(key=lambda e: e["time"])

        return all_units, unit_events, pd.DataFrame(resource_events)

    # ephemeral unit are units like NovaGriffinBombingRunTargeter, NovaGriffinBombingRunStrafer, LocustFlying, ToxicNest, NovaBoombotBurrowed
    # When we compute army value we want to avoid these units. These unites are has short live,
    # some of them comes with huge numbers which will affect the army value report.
    #
    #
    #
    def temporary_units(self, all_units: dict[int, Unit],min_instances=3)->DataFrame:
        rows = []

        for unit in all_units.values():

            if unit.is_army:
                continue

            if unit.death_frame is None:
                continue

            lifetime = (
                    unit.death_frame
                    - unit.birth_frame
            )

            rows.append({
                "unit_type": unit.current_type,
                "lifetime": lifetime
            })

        lifetimes_df = pd.DataFrame(rows)

        report = (
            lifetimes_df
            .groupby("unit_type", as_index=False)
            .agg(
                instances=("lifetime", "count"),
                avg_lifetime=("lifetime", "mean"),
                median_lifetime=("lifetime", "median"),
                min_lifetime=("lifetime", "min"),
                max_lifetime=("lifetime", "max"),
                p90_lifetime=("lifetime",
                              lambda x: x.quantile(.9)),
            )
        )

        report["is_ephemeral"] = (
                (report["instances"] >= 10)
                &
                (report["median_lifetime"] < 15)
                &
                (report["p90_lifetime"] < 20)
        )

        report["temporary_score"] = (
                (report["median_lifetime"] < 15).astype(int) * 3
                + (report["p90_lifetime"] < 30).astype(int) * 3
                + (report["instances"] > 50).astype(int)
        )

        report["is_temporary"] = report["temporary_score"] >= 6

        report = report[
            report["instances"] >= min_instances
            ]

        return report.sort_values(
            "median_lifetime"
        )


    def ephemeral_units(self, all_units: dict[int, Unit], min_instances=10) -> set[str]:

        report = self.temporary_units(
            all_units,
            min_instances
        )

        return set(
            report.loc[
                report["is_ephemeral"],
                "unit_type"
            ]
        )

    def temporary_units_set(self, all_units: dict[int, Unit], min_instances=10) -> set[str]:

        report = self.temporary_units(
            all_units,
            min_instances
        )

        return set(
            report.loc[
                report["is_temporary"],
                "unit_type"
            ]
        )

