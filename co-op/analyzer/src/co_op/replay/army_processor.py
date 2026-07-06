import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame
from sc2reader.resources import Replay
from models.unit import Unit
from models.unit_cost import UnitCost, UNIT_COSTS
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
        army_value_timeline = dict()
        # unit_type key, unit_cost is the value
        unit_cost_dict = dict()
        # contain list of units born between PlayerStatsEvent where key is player_id
        army_unit_born_dict = dict()

        old_mineral = dict()
        old_gas = dict()
        current_mineral = dict()
        current_gas = dict()
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

                if event.name == "UnitBornEvent" and (unit_types.is_race_army() or unit_types.is_commander_unit() or unit_types.is_commander()):
                    old_list = army_unit_born_dict.get(owner, [])
                    old_list.append({
                        "unit_type": event.unit_type_name,
                        "unit_id": event.unit_id,
                        "player_id": owner,
                        "frame": event.frame,
                    })
                    army_unit_born_dict[owner] = old_list

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
                player_id = event.pid
                if player_id is None or player_id == 0 or not player_id in players:
                    continue
                # old_gas[player_id] = current_gas.get(player_id, 0)
                # old_mineral[player_id] = current_mineral.get(player_id, 0)
                # current_gas[player_id] = event.vespene_used_current_army
                # current_mineral[player_id] = event.minerals_used_current_army
                #
                # army_units = army_unit_born_dict.get(player_id, None) #
                # self.compute_unit_cost(unit_cost_dict, army_units,
                #                        old_gas.get(player_id, 0), old_mineral.get(player_id, 0),
                #                        current_gas.get(player_id, 0), current_mineral.get(player_id, 0))
                # army_unit_born_dict[event.pid] = []

                minerals = event.minerals_used_current_army
                gas = event.vespene_used_current_army
                old = army_value_timeline.get(player_id, [])
                old.append( {
                    "seconds": event.second,
                    "player_id": player_id,
                    "minerals": minerals,
                    "gas": gas,
                    "total": minerals + gas,
                })
                army_value_timeline[player_id] = old

                resource_events.append({
                    "frame": event.frame,
                    "time": event.second,
                    "player_id": player_id,
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

        result = {
            "all_units": all_units,
            "unit_events": unit_events,
            "resource_events": pd.DataFrame(resource_events),
            "army_value_timeline": army_value_timeline,
        }

        return result

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

    def compute_unit_cost(self, unit_cost_dict, army_units, old_gas, old_mineral, current_gas,
                          current_mineral, call_number=1):
        if army_units == None or len(army_units) == 0:
            return
        # step: 1
        # If army unite items has the same unit type, or has single item
        all_same = len({p["unit_type"]  for p in army_units}) <= 1
        if len(army_units) == 1 or all_same:
            unit = army_units[0]
            unit_type = unit["unit_type"]
            gas = max((current_gas - old_gas), 0)/len(army_units)
            mineral = max((current_mineral - old_mineral), 0)/len(army_units)

            # Notice: this will be always the source of truth, so that is why it is ok to override old value if exists
            unit_cost_dict[unit_type] =  UnitCost('unit_type', mineral, gas, 0.0)
            return


        avg_mineral = current_mineral /len(army_units)
        avg_gas = current_gas /len(army_units)

        new_mineral = current_mineral
        new_gas = current_gas
        new_army_list = []
        for unit in army_units:
            unit_type = unit["unit_type"]
            unit_cost = unit_cost_dict.get(unit_type, None)
            if unit_cost is not None:
                current_mineral -= unit_cost.minerals
                current_gas -= unit_cost.gas

                new_mineral -= unit_cost.mineral
                new_gas -= unit_cost.gas
                continue  # unit cost already exist no need to compute it

            unit_cost = UNIT_COSTS.get(unit_type, None)
            if unit_cost is not None:
                current_mineral -= unit_cost.mineral
                current_gas -= unit_cost.gas

                new_mineral -= unit_cost.mineral
                new_gas -= unit_cost.gas
                continue

            # Now these calculations are wrong, we will debends that this can be fixed later(step 1)
            # We must do this, at least we have some values even if they are not exact
            if call_number != 1:
                unit_cost_dict[unit_type] = UnitCost('unit_type', avg_mineral, avg_gas, 0.0)
            current_mineral -= avg_mineral
            current_gas -= avg_gas
            new_army_list.append(unit)  # this will be used for the second call

        if call_number == 1:
            # call the method again to try
            self.compute_unit_cost(unit_cost_dict, new_army_list, old_gas, old_mineral, new_gas,
                                   new_mineral, 2)
