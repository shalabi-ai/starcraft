from collections import Counter, defaultdict

from models.player import Player


class ReplayAnalyser:
    def __init__(
            self,
            players: dict[int, Player],
            kills,
            kill_events
    ):
        self.players = players
        self.kills = kills
        self.kill_events = kill_events


    def top_units(self, limit: int = 20):
        counter = Counter()

        for event in self.kill_events:
            counter[(event["killer_unit"], event["killer_player"])] += 1

        return counter.most_common(limit)

    def top_victims(self, limit: int = 20):
        counter = Counter()

        for event in self.kill_events:
            counter[(event["victim_unit"], event["killer_player"])] += 1

        return counter.most_common(limit)

    def commander_kills(self):
        result = defaultdict(int)

        for event in self.kill_events:
            player_id = event["killer_player"]

            player = self.players.get(player_id)
            if not player:
                continue

            result[player.commander] += 1

        return dict(sorted(
            result.items(),
            key=lambda x: x[1],
            reverse=True
    ))

    def commander_breakdown(self):
        result = defaultdict(lambda: defaultdict(int))

        for event in self.kill_events:
            player = self.players.get(event["killer_player"])

            if not player:
                continue

            commander = player.commander
            unit = event["killer_unit"]

            result[commander][unit] += 1

        return result