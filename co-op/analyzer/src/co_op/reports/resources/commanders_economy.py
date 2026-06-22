import pandas as pd
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
from pandas import DataFrame

from replay import economy_processor
from replay.economy_processor import EconomyProcessor
from replay.replay_factory import ReplayFactory
from reports.resources.economy_report import EconomyReport


class CommandersEconomyReport(EconomyReport):
    # get tracker_events from ReplayFactory.replay_from_s2protocol
    def __init__(self, file_path):
        super().__init__(file_path)

    def plot(self, ax: Axes, df: DataFrame, player_name: str):
        ax.plot(
            df["seconds"],
            df["minerals_collection_rate"],
            label="Mineral Income"
        )

        ax.plot(
            df["seconds"],
            df["vespene_collection_rate"],
            label="Gas Income"
        )

        ax.set_title(player_name + " Income Rate")
        ax.set_xlabel("Seconds")
        ax.set_ylabel("Resources / Minute")
        ax.legend()
