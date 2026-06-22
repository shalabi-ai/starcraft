from matplotlib.axes import Axes
from models.player import Player
from replay import economy_processor
from replay.economy_processor import EconomyProcessor
import matplotlib.pyplot as plt
from replay.replay_factory import ReplayFactory

class CommandersEconomyReport:
    # get tracker_events from ReplayFactory.replay_from_s2protocol
    def __init__(self, file_path):
        self.file_path = file_path

    def report(self, players: list[Player]):
        fig, axes = plt.subplots(
            1,
            len(players),
            figsize=(8 * (len(players) + 1), 7)
        )

        tracker_events = list(
            ReplayFactory.replay_from_s2protocol(self.file_path)
        )
        economy_processor = EconomyProcessor(tracker_events)
        for player, ax in zip(players, axes):


            df = economy_processor.extract_player_stats(tracker_events, player.id)
            CommandersEconomyReport.plot(ax, df, player.name)

        plt.tight_layout()
        plt.show()

    def show(self, players: list[Player]):

        for player in players:
            # we can not process the tracker_events more than once
            tracker_events = ReplayFactory.replay_from_s2protocol(self.file_path)
            economy_processor = EconomyProcessor(tracker_events)

            df = economy_processor.extract_player_stats(tracker_events, player.id)
            CommandersEconomyReport.plot_income(df, player.name)

    @staticmethod
    def plot_income(df, player_name):

        fig, ax = plt.subplots(figsize=(12, 6))

        CommandersEconomyReport.plot(ax, df, player_name)

        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot(ax: Axes, df, player_name):
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
