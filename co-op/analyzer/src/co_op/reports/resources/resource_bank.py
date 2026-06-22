from matplotlib.axes import Axes
from models.player import Player
from pandas import DataFrame
from replay import economy_processor
from replay.economy_processor import EconomyProcessor
import matplotlib.pyplot as plt
from replay.replay_factory import ReplayFactory
from matplotlib.patches import Patch
from reports.resources.economy_report import EconomyReport
from reports.resources.resource_bank_analysis_model import ResourceBankAnalysisModel
from reports.resources.resource_bank_analysis import ResourceBankAnalysis

class ResourceBankReport(EconomyReport):
   #def __init__(self, tracker_events):
   #     super().__init__(tracker_events)

    def plot(self, ax: Axes, player_df: DataFrame, player_name: str):
        p = (
            player_df
            .sort_values("seconds")
            .reset_index(drop=True)
            .copy()
        )
        if p.empty:
            return
        analysis = ResourceBankAnalysis(p)
        model = analysis.get_resource_bank()

        # ====================================
        # Plot
        # ====================================

        minerals_line, = ax.plot(
            p["seconds"],
            p["minerals_current"],
            label="Minerals Bank",
            linewidth=2
        )

        gas_line,  = ax.plot(
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

        self.fill_region(ax, p)

        ax.set_title(
            f"{player_name} (Grade {model.grade})"
        )

        ax.set_xlabel("Seconds")
        ax.set_ylabel("Resources")

        ax.grid(True, alpha=0.25)

        stats_text = self.get_analysis_text(model)

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
            minerals_line,
            gas_line,
            Patch(alpha=0.08, label="High Float (>2000M)")
        ]

        ax.legend(handles=legend_handles, loc="upper left")

    @staticmethod
    def get_analysis_text(model: ResourceBankAnalysisModel) -> str:
        stats_text = (
            f"Game Duration       {model.game_minutes:6.1f}\n"
            f"Grade       {model.grade}\n"
            f"Spend Efficiency    {model.spend_efficiency:6.1f}%\n"
            f"Avg Float  {model.avg_float:8,.1f}\n" # custom metric measuring how much resource float accumulated over time. higher value means worse spending discipline.
            f"\nCollected\n"
            # f"Avg Float   {avg_float:8,.0f}\n"
            f"M     {model.total_minerals_collected:,.0f}\n"
            f"G     {model.total_gas_collected:,.0f}\n"
            f"\nSpent\n"
            f"M     {model.spent_minerals:,.0f}\n"
            f"G     {model.spent_gas:,.0f}\n"
            f"\nAvg Bank\n"
            f"M       {model.avg_minerals:8,.0f}\n"
            f"G       {model.avg_gas:8,.0f}\n"
            f"\nFinal Bank\n"
            f"M     {model.final_minerals:8,.0f}\n"
            f"G     {model.final_gas:8,.0f}\n"
            f"\nPeak Income/min\n"
            f"M       {model.peak_minerals_collection_rate:8,.0f}\n"
            f"G       {model.peak_gas_collection_rate:8,.0f}"
        )
        return stats_text

    @staticmethod
    def fill_region(ax: Axes, p:DataFrame):
        high_float = (p["minerals_current"] + p["vespene_current"]) > 2000

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