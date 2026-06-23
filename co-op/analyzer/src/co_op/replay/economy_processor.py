import pandas as pd
from s2protocol import versions
from mpyq import MPQArchive

from replay import FRAME_RATE


class EconomyProcessor:
    def __init__(self, tracker_events):
        self.tracker_events = tracker_events

    def extract_player_stats(self, player_id):
        """
        Extract all SPlayerStatsEvent rows.
        """

        rows = []

        for event in self.tracker_events:

            if event.get("_event") != "NNet.Replay.Tracker.SPlayerStatsEvent":
                continue

            if event["m_playerId"] != player_id:
                continue

            stats = event["m_stats"]

            rows.append(
                {
                    "seconds": event["_gameloop"] / FRAME_RATE,

                    "minerals_current":
                        stats.get("m_scoreValueMineralsCurrent", 0),

                    "vespene_current":
                        stats.get("m_scoreValueVespeneCurrent", 0),

                    "minerals_collection_rate":
                        stats.get("m_scoreValueMineralsCollectionRate", 0),

                    "vespene_collection_rate":
                        stats.get("m_scoreValueVespeneCollectionRate", 0),

                    "workers_active":
                        stats.get("m_scoreValueWorkersActiveCount", 0),

                    "minerals_used_army":
                        stats.get("m_scoreValueMineralsUsedCurrentArmy", 0),

                    "vespene_used_army":
                        stats.get("m_scoreValueVespeneUsedCurrentArmy", 0),

                    "minerals_used_economy":
                        stats.get("m_scoreValueMineralsUsedCurrentEconomy", 0),

                    "vespene_used_economy":
                        stats.get("m_scoreValueVespeneUsedCurrentEconomy", 0),

                    "minerals_used_technology":
                        stats.get("m_scoreValueMineralsUsedCurrentTechnology", 0),

                    "vespene_used_technology":
                        stats.get("m_scoreValueVespeneUsedCurrentTechnology", 0),
                }
            )

        return pd.DataFrame(rows)