import numpy as np
from matplotlib import pyplot as plt
from pandas import DataFrame


class ResourceEfficiencyReport:
    def __init__(self, df: DataFrame):
        self.df = self._prepare_data(df)

    def plot_resource_efficiency(self):
        # Plot Resource Efficiency and Net Resource Efficiency
        #         for each player in separate subplots.


        # when gas and mineral lost is zero Resource Efficiency will not show any thing.
        # self.plot_resource("Resource Efficiency", "resource_efficiency")
        self.plot_resource("Net Resource Efficiency", "net_resource_efficiency")
    def plot_resource(self, title: str, field: str):
        df = self.df
        players = sorted(df["player_id"].unique())

        fig, axes = plt.subplots(
            nrows=len(players),
            ncols=1,
            figsize=(12, 5 * len(players)),
            sharex=True
        )

        if len(players) == 1:
            axes = [axes]

        for ax, player in zip(axes, players):
            player_df = (
                df[df["player_id"] == player]
                .sort_values("time")
            )

            ax.plot(
                player_df["time"],
                player_df[field],
                label=title,
                linewidth=2
            )

            ax.set_title(f"Player {player}")
            ax.set_ylabel("Efficiency")
            ax.grid(True, alpha=0.3)
            ax.legend()

        axes[-1].set_xlabel("Time")

        plt.tight_layout()
        plt.show()

    def _prepare_data(self, df: DataFrame)->DataFrame:
        # Total resources killed and lost
        #df = (
        #    resources
        #    .sort_values("seconds")
        #    .reset_index(drop=True)
        #    .copy()
        #)
        df = df.sort_values(["player_id", "time"])
        df["resources_killed"] = (df["minerals_killed"] + df["vespene_killed"])
        df["resources_lost"] = (df["minerals_lost"] + df["vespene_lost"])

        # Resource Efficiency
        # Handle division-by-zero cases
        df["resource_efficiency"] = np.where(
            df["resources_lost"] > 0,
            df["resources_killed"] / df["resources_lost"],
            np.nan
        )

        # replace NaN with 0 or infinity
        df["resource_efficiency"] = df["resource_efficiency"].fillna(0)

        # Net Resource Efficiency
        #
        # If you want a metric centered around advantage gained rather than a ratio:
        #
        # Net Resource Efficiency=(minerals_killed+vespene_killed)−(minerals_lost+vespene_lost)
        #df = df.sort_values(["player_id", "time"])
        df["net_resource_efficiency"] = (
                df["minerals_killed"] + df["vespene_killed"]
                - df["minerals_lost"] - df["vespene_lost"]
        )

        return df
