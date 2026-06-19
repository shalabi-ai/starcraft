from sc2reader.resources import Replay

from co_op.models.player import Player


class CoOpReplay:
    def __init__(self, replay: Replay):
        self.replay = replay

    def getPlayers(self)->list[Player]:
        players = []
        for client in self.replay.clients:
            if client.is_human:
                player = Player(id=client.pid, name=client.name, commander=client.commander, race=client.play_race, events=client.events)
                players.append(player)
        return players

    def getPlayerMap(self) -> dict[int, Player]:
        return {
            client.pid: Player(
                id=client.pid,
                name=client.name,
                commander=client.commander,
                race=client.play_race,
                events=client.events
            )
            for client in self.replay.clients
            if client.is_human
        }

