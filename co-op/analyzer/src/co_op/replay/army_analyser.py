from collections import defaultdict

import pandas as pd
from pandas import DataFrame
from replay import unit_value
from replay.unit_value import UnitValue


class ArmyAnalyser:
    def __init__(self, unit_events, players):
        self.unit_events = unit_events
        self.players = players

    def army_state_timeline(self, snapshot_interval_seconds=30):

        current_army = defaultdict(
            lambda: defaultdict(int)
        )

        rows = []

        events = sorted(
            self.unit_events,
            key=lambda e: e["time"]
        )

        next_snapshot = 0

        for event in events:

            player = event["player"]
            if player not in self.players:
                continue
            current_time = event["time"]

            # -------------------------
            # Update state
            # -------------------------

            if event["action"] == "born":

                player = event["player"]
                unit_type = event["unit_type"]

                current_army[player][unit_type] += 1

            elif event["action"] == "died":

                player = event["player"]
                unit_type = event["unit_type"]

                current_army[player][unit_type] -= 1

                if current_army[player][unit_type] <= 0:
                    del current_army[player][unit_type]

            elif event["action"] == "morph":

                player = event["player"]

                old_type = event["old_type"]
                new_type = event["new_type"]

                current_army[player][old_type] -= 1

                if current_army[player][old_type] <= 0:
                    del current_army[player][old_type]

                current_army[player][new_type] += 1

            # -------------------------
            # Emit snapshots
            # -------------------------

            while current_time >= next_snapshot:

                for player_id, army in current_army.items():

                    commander = self.players[player_id].commander

                    for unit_type, count in army.items():

                        rows.append({
                            "time": next_snapshot,
                            "player": player_id,
                            "commander": commander,
                            "unit_type": unit_type,
                            "count": count
                        })

                next_snapshot += snapshot_interval_seconds

        return pd.DataFrame(rows)


    def army_value_timeline(self, snapshot_interval_seconds=30)->pd.DataFrame:
        rows = []
        current_army_value = defaultdict(int)
        unit_value = UnitValue()

        events = sorted(
            self.unit_events,
            key=lambda e: e["time"]
        )

        if not events:
            return pd.DataFrame(
                columns=[
                    "time",
                    "player",
                    "commander",
                    "army_value"
                ]
            )

        next_snapshot = 0

        for event in events:
            player = event["player"]
            if player not in self.players:
                continue

            current_time = event["time"]

            while current_time >= next_snapshot:
                for player_id in self.players:

                    rows.append({
                        "time": next_snapshot,
                        "player": player_id,
                        "commander": self.players[player_id].commander,
                        "army_value": current_army_value[player_id]
                    })

                next_snapshot += snapshot_interval_seconds

            if event["action"] == "born":
                unit = event["unit_type"]
                current_army_value[player] += unit_value.get(unit)

            elif event["action"] == "died":
                unit = event["unit_type"]
                current_army_value[player] -= unit_value.get(unit)

            elif event["action"] == "morph":
                old_type = event["old_type"]
                new_type = event["new_type"]
                current_army_value[player] += (
                        unit_value.get(new_type)
                        - unit_value.get(old_type)
                )

        # ----------------------------------
        # Final snapshot
        # ----------------------------------
        final_time = events[-1]["time"]

        while next_snapshot <= final_time:
            for player_id in self.players:
                rows.append({
                    "time": next_snapshot,
                    "player": player_id,
                    "commander":
                        self.players[player_id].commander,
                    "army_value":
                        current_army_value[player_id]
                })

            next_snapshot += (
                snapshot_interval_seconds
            )
        return pd.DataFrame(rows)

    def create_delta_events(self, df1: DataFrame):
        df = df1.copy(True)
        df = df.sort_values(
            ["player", "unit_type", "time"]
        )

        df["prev_count"] = (
            df.groupby(["player", "unit_type"])["count"]
            .shift(1)
            .fillna(0)
        )

        df["delta"] = df["count"] - df["prev_count"]

        births = df[df["delta"] > 0].copy()
        births["event"] = "born"
        births["amount"] = births["delta"]

        deaths = df[df["delta"] < 0].copy()
        deaths["event"] = "died"
        deaths["amount"] = -deaths["delta"]

        events = pd.concat([
            births,
            deaths
        ]).sort_values("time")

        return events