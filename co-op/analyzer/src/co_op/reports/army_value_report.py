from pathlib import Path

import matplotlib.pyplot as plt

from models.player import Player


class ArmyValueReport:
    def plot_army_value_timeline(self,
            timeline_by_player: dict[int, list[dict]],
            players,
            output_file: str | None = None,
        ):

        plt.figure(figsize=(12, 6))

        for player_id in players:
            player = players[player_id]
            timeline = timeline_by_player[player.id]
            if not timeline:
                continue

            x = [point["seconds"] for point in timeline]
            y = [point["total"] for point in timeline]

            plt.plot(
                x,
                y,
                label=f"{player.commander} ({player.name})",
                linewidth=2,
            )


        plt.title("Army Value (Minerals + Gas Invested)")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Army Value (Minerals + Gas)")
        plt.grid(True, alpha=0.3)
        plt.legend()

        plt.tight_layout()
        plt.show()

        if output_file:
            Path(output_file).parent.mkdir(
                parents=True,
                exist_ok=True,
            )
            plt.savefig(output_file, dpi=150)

        return plt.gcf()
    def plot_army_value_timeline1(self, df):

        plt.figure(figsize=(12, 6))

        for player, player_df in df.groupby("player"):
            commander = player_df["commander"].iloc[0]

            plt.plot(
                player_df["time"],
                player_df["army_value"],
                label=f"{commander} ({player})"
            )

        plt.title("Army Value (Minerals + Gas Invested)")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Army Value")
        plt.grid(True)
        plt.legend()

        plt.tight_layout()
        plt.show()