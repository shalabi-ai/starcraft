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

    def kill_timeline(self):
        timeline = defaultdict(int)

        for event in self.kill_events:
            minute = int(event["time"] / (22.4 * 60))
            timeline[minute] += 1

        return dict(sorted(timeline.items()))

    def kill_timeline_by_commander(self):
        timeline = defaultdict(lambda: defaultdict(int))

        for event in self.kill_events:
            minute = int(event["time"] / (22.4 * 60))

            player = self.players.get(event["killer_player"])
            if not player:
                continue

            timeline[player.commander][minute] += 1

        return timeline

    def commander_report(self, top_n: int = 20) -> str:
        commander_stats = defaultdict(lambda: defaultdict(int))
        commander_totals = defaultdict(int)

        for event in self.kill_events:
            player = self.players.get(event["killer_player"])

            if not player:
                continue

            commander = player.commander
            unit = event["killer_unit"]

            commander_stats[commander][unit] += 1
            commander_totals[commander] += 1

        lines = []

        for commander, total_kills in sorted(
                commander_totals.items(),
                key=lambda x: x[1],
                reverse=True
        ):
            lines.append(f"{commander}")
            lines.append("=" * len(str(commander)))
            lines.append(f"Total Kills: {total_kills}")
            lines.append("")

            units = sorted(
                commander_stats[commander].items(),
                key=lambda x: x[1],
                reverse=True
            )

            for unit, count in units[:top_n]:
                lines.append(f"{unit:<35} {count}")

            lines.append("")
            lines.append("")

        return "\n".join(lines)