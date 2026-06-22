from matplotlib.axes import Axes
from models.player import Player
from pandas import DataFrame
from replay import economy_processor
from replay.economy_processor import EconomyProcessor
import matplotlib.pyplot as plt
from replay.replay_factory import ReplayFactory
from matplotlib.patches import Patch

class ResourceBankReport:
    def __init__(self, file_path):
        self.file_path = file_path


    def report(self, players: list[Player]):
        fig, axes = plt.subplots(
            1,
            len(players),
            figsize=(12 * len(players), 7),
            squeeze=False
        )
        axes = axes.flatten()

        tracker_events = list(
            ReplayFactory.replay_from_s2protocol(self.file_path)
        )
        economy_processor = EconomyProcessor(tracker_events)
        for player, ax in zip(players, axes):
            df = economy_processor.extract_player_stats(tracker_events, player.id)
            #df.sort_values("seconds")
            ResourceBankReport.plot(ax, df, player.name)

        plt.suptitle(
            "Resource Bank Analysis",
            fontsize=16
        )
        plt.subplots_adjust(right=0.85)
        plt.tight_layout()
        plt.show()


    @staticmethod
    def economy_grade(score):
        if score < 100:
            return "A"
        elif score < 250:
            return "B"
        elif score < 500:
            return "C"
        else:
            return "D"

    @staticmethod
    def plot(ax: Axes, player_df, player_name):
        p = (
            player_df
            .sort_values("seconds")
            .reset_index(drop=True)
            .copy()
        )

        # ====================================
        # Metrics
        # ====================================

        p["float_score"] = (
                p["minerals_current"]
                + 2.0 * p["vespene_current"]
        )

        avg_float = p["float_score"].mean()

        avg_minerals = p["minerals_current"].mean()
        avg_gas = p["vespene_current"].mean()

        max_minerals = p["minerals_current"].max()
        max_gas = p["vespene_current"].max()

        final_minerals = p["minerals_current"].iloc[-1]
        final_gas = p["vespene_current"].iloc[-1]

        pct_above_1000 = (
                (p["minerals_current"] > 1000).mean() * 100
        )

        pct_above_2000 = (
                (p["minerals_current"] > 2000).mean() * 100
        )

        pct_above_3000 = (
                (p["minerals_current"] > 3000).mean() * 100
        )

        # Float Area (integral)
        dt = p["seconds"].diff().fillna(0)

        float_area = (
                p["float_score"] * dt
        ).sum()


        game_length = max(p["seconds"].max(), 1)

        float_score = (
                              (float_area / game_length) * 60
                      ) / 1000
        grade = ResourceBankReport.economy_grade(float_score)


        # ====================================
        # Plot
        # ====================================

        ax.plot(
            p["seconds"],
            p["minerals_current"],
            label="Minerals Bank",
            linewidth=2
        )

        ax.plot(
            p["seconds"],
            p["vespene_current"],
            label="Gas Bank",
            linewidth=2
        )

        ymax = max(
            p["minerals_current"].max(),
            p["vespene_current"].max()
        ) * 1.05

        # Resource float zones
        ax.axhspan(0, min(1000, ymax), alpha=0.03)

        if ymax > 1000:
            ax.axhspan(
                1000,
                min(2000, ymax),
                alpha=0.05
            )

        if ymax > 2000:
            ax.axhspan(
                2000,
                ymax,
                alpha=0.08
            )

        # Thresholds
        ax.axhline(
            1000,
            linestyle="--",
            alpha=0.35
        )

        ax.axhline(
            2000,
            linestyle=":",
            alpha=0.35
        )

        ResourceBankReport.fill_region(ax, p)

        ax.set_title(
            f"{player_name} (Grade {grade})"
        )

        ax.set_xlabel("Seconds")
        ax.set_ylabel("Resources")

        ax.grid(True, alpha=0.25)

        total_minerals_collected = (
                (p["minerals_collection_rate"] / 60) * dt
        ).sum()

        # Collection Rate = resources/minute
        # ÷ 60            = resources/second
        # × dt            = resources collected during interval
        # 1200 minerals/min
        # 20 seconds
        #
        # becomes:
        #
        # 1200 / 60 = 20 minerals/sec
        #
        # 20 × 20 = 400 minerals collected
        total_gas_collected = (
                (p["vespene_collection_rate"] / 60) * dt
        ).sum()

        final_bank = (
                final_minerals +
                final_gas
        )

        total_collected = (
                total_minerals_collected +
                total_gas_collected
        )

        weighted_bank = (
                final_minerals +
                2 * final_gas
        )

        weighted_collected = (
                total_minerals_collected +
                2 * total_gas_collected
        )

        spend_efficiency = (
                100 *
                (1 - weighted_bank / weighted_collected)
        )

        peak_m_income = p["minerals_collection_rate"].max()
        peak_g_income = p["vespene_collection_rate"].max()

        game_minutes = p["seconds"].max() / 60

        spent_minerals = total_minerals_collected - final_minerals
        spent_gas = total_gas_collected - final_gas

        stats_text = (
            f"Game Duration       {game_minutes:6.1f}\n"
            f"Grade       {grade}\n"
            f"SpendEfficiency    {spend_efficiency:6.1f}%\n"
            f"FloatScore  {float_score:8,.1f}\n"
            f"\nCollected\n"
           # f"Avg Float   {avg_float:8,.0f}\n"
            f"M     {total_minerals_collected:,.0f}\n"
            f"G     {total_gas_collected:,.0f}\n"
            f"\nSpent\n"
            f"M     {spent_minerals:,.0f}\n"
            f"G     {spent_gas:,.0f}\n"
            f"\nAvg Bank\n"
            f"M       {avg_minerals:8,.0f}\n"
            f"G       {avg_gas:8,.0f}\n"
            f"\nFinal Bank\n"
            f"M     {final_minerals:8,.0f}\n"
            f"G     {final_gas:8,.0f}\n"
            f"\nPeak Income/min\n"
            f"M       {peak_m_income:8,.0f}\n"
            f"G       {peak_g_income:8,.0f}"
        )

        ax.text(
            1.02,
            0.98,
            stats_text,
            transform=ax.transAxes,
            va="top",
            ha="left",
            fontsize=9,
            fontfamily="monospace",
            bbox=dict(alpha=0.85)
        )

        legend_handles = [
            ax.lines[0],
            ax.lines[1],
            Patch(alpha=0.08, label="High Float (>2000M)")
        ]

        ax.legend(handles=legend_handles, loc="upper left")

    @staticmethod
    def fill_region(ax, p:DataFrame):
        high_float = p["minerals_current"] > 2000

        start = None

        for i, flag in enumerate(high_float):

            if flag and start is None:
                start = p["seconds"].iloc[i]

            elif not flag and start is not None:
                end = p["seconds"].iloc[i]

                ax.axvspan(
                    start,
                    end,
                    alpha=0.08
                )

                start = None

        if start is not None:
            ax.axvspan(
                start,
                p["seconds"].iloc[-1],
                alpha=0.08
            )