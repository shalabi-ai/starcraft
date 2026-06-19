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

    def plot_commanders_chart(self, top_n: int=6):
        # commanders = self.commanders_data["commander"].unique()
        compare_df = self.commander_compare()
        commanders = compare_df["commander"].tolist()

        fig, axes = plt.subplots(
            1,
            len(commanders) + 1,
            figsize=(8 * (len(commanders) + 1), 7)
        )

        if len(commanders) == 1:
            axes = [axes]

        # -------------------------
        # Commander pie charts
        # -------------------------
        for i, commander in enumerate(commanders):

            df = self.by_commander(commander)

            # Keep top N units
            top = df.head(top_n).copy()

            # Aggregate the rest into "Other"
            if len(df) > top_n:
                other_kills = df.iloc[top_n:]["kills"].sum()

                if other_kills > 0:
                    other_pct = df.iloc[top_n:]["percentage"].sum()

                    top = pd.concat([
                        top,
                        pd.DataFrame([{
                            "unit": "Other",
                            "kills": other_kills,
                            "percentage": other_pct
                        }])
                    ], ignore_index=True)

            wedges, _, _ = axes[i].pie(
                top["kills"],
                labels=None,
                autopct="%1.1f%%",
                startangle=90
            )

            total = int(df["kills"].sum())

            axes[i].set_title(
                f"{commander}\n{total:,} kills"
            )

            axes[i].legend(
                wedges,
                top["unit"],
                title="Units",
                loc="center left",
                bbox_to_anchor=(1.0, 0.5)
            )

        # -------------------------
        # Commander comparison
        # -------------------------
        compare_df = self.commander_compare()

        bars = axes[-1].bar(
            compare_df["commander"],
            compare_df["kills"]
        )

        axes[-1].set_title("Commander Total Kills")
        axes[-1].set_ylabel("Kills")

        # Show values on bars
        for bar in bars:
            height = bar.get_height()

            axes[-1].text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{int(height):,}",
                ha="center",
                va="bottom"
            )

        plt.tight_layout()
        plt.show()