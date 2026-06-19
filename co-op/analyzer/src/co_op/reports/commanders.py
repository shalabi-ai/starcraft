import pandas as pd
import matplotlib.pyplot as plt
from replay.analyser import ReplayAnalyser

class Commanders:
    def __init__(self, analyser: ReplayAnalyser):
        self.analyser = analyser
        self.commanders_data = self.commanders_report()

    def commanders_report(self):
        rows = []

        breakdown = self.analyser.commander_breakdown()

        for commander, units in breakdown.items():
            for unit, kills in units.items():
                rows.append({
                    "commander": commander,
                    "unit": unit,
                    "kills": kills
                })

        return pd.DataFrame(rows)

    def by_commander(self, commander: str):
        df = self.commanders_data

        df = df[df["commander"] == commander].copy()

        total = df["kills"].sum()

        df["percentage"] = (
                df["kills"] / total * 100
        )

        return df.sort_values(
            "percentage",
            ascending=False
        )

    def commander_compare(self):
        df = self.commanders_data

        return (
            df.groupby("commander", as_index=False)
            .agg(kills=("kills", "sum"))
            .sort_values("kills", ascending=False)
        )

    def plot_commanders_chart(self):
        commanders = self.commanders_data["commander"].unique()

        fig, axes = plt.subplots(
            1,
            len(commanders) + 1,
            figsize=(7 * (len(commanders) + 1), 7)
        )

        if len(commanders) == 1:
            axes = [axes]

        # Pie charts
        for i, commander in enumerate(commanders):
            df = self.by_commander(commander)

            axes[i].pie(
                df["kills"],
                labels=df["unit"],
                autopct="%1.1f%%"
            )

            total = int(df["kills"].sum())

            axes[i].set_title(
                f"{commander}\n{total} kills"
            )

        # Commander comparison
        compare_df = self.commander_compare()

        axes[-1].bar(
            compare_df["commander"],
            compare_df["kills"]
        )

        axes[-1].set_title("Commander Total Kills")
        axes[-1].set_ylabel("Kills")

        plt.tight_layout()
        plt.show()