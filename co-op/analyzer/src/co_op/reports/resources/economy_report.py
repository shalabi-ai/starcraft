from matplotlib import pyplot as plt
from models.player import Player
from pandas import DataFrame
from replay.replay_factory import ReplayFactory
from replay.economy_processor import EconomyProcessor

from abc import ABC, abstractmethod

class EconomyReport(ABC):
    def __init__(self, tracker_events):
        self.tracker_events = tracker_events

    def generate_report(self, players: list[Player]):
        _, axes = plt.subplots(
            1,
            len(players),
            figsize=(8 * (len(players) + 1), 7)
        )
        if len(players) == 1:
            axes = [axes]

        economy_processor = EconomyProcessor(self.tracker_events)
        for player, ax in zip(players, axes):
            df = economy_processor.extract_player_stats(player.id)
            self.plot(ax, df, player.name)

        plt.tight_layout()
        plt.show()

    @abstractmethod
    def plot(self, ax: plt.Axes, df: DataFrame, player_name: str):
        pass