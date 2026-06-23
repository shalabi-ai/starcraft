import matplotlib.pyplot as plt

class ArmyValueReport:
    def plot_army_value_timeline(self, df):

        plt.figure(figsize=(12, 6))

        for player, player_df in df.groupby("player"):

            commander = player_df["commander"].iloc[0]

            plt.plot(
                player_df["time"],
                player_df["army_value"],
                label=f"{commander} (P{player})"
            )

        plt.title("Army Value Timeline")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Army Value")
        plt.grid(True)
        plt.legend()

        plt.tight_layout()
        plt.show()