from matplotlib.axes import Axes
from pandas import DataFrame
from reports.resources.economy_report import EconomyReport

class CommandersEconomyReport(EconomyReport):
    # get tracker_events from ReplayFactory.replay_from_s2protocol
    #def __init__(self, tracker_events):
    #    super().__init__(tracker_events)

    def plot(self, ax: Axes, df: DataFrame, player_name: str):
        ax.plot(
            df["seconds"],
            df["minerals_collection_rate"],
            label="Mineral Income",
            linewidth=2
        )

        ax.plot(
            df["seconds"],
            df["vespene_collection_rate"],
            label="Gas Income",
            linewidth=2
        )

        peak_m = df["minerals_collection_rate"].max()
        peak_g = df["vespene_collection_rate"].max()

        ax.set_title(
            f"{player_name} Income Rate\n"
            f"Peak M: {peak_m:.0f}  Peak G: {peak_g:.0f}"
        )

        ax.set_xlabel("Seconds")
        ax.set_ylabel("Resources / Minute")
        ax.grid(True, alpha=0.3)
        ax.legend()
