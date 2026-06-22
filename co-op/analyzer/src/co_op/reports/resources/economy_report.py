from matplotlib import pyplot as plt
from models.player import Player
from pandas import DataFrame
from replay.replay_factory import ReplayFactory
from replay.economy_processor import EconomyProcessor


class EconomyReport:
    def __init__(self, file_path):
        self.file_path = file_path

    def generate_report(self, players: list[Player]):
        fig, axes = plt.subplots(
            1,
            len(players),
            figsize=(8 * (len(players) + 1), 7)
        )
        if len(players) == 1:
            axes = [axes]

        tracker_events = list(
            ReplayFactory.replay_from_s2protocol(self.file_path)
        )
        economy_processor = EconomyProcessor(tracker_events)
        for player, ax in zip(players, axes):
            df = economy_processor.extract_player_stats(player.id)
            self.plot(ax, df, player.name)

        plt.tight_layout()
        plt.show()

    def plot(self, ax: plt.Axes, df: DataFrame, player_name: str):
        raise NotImplementedError