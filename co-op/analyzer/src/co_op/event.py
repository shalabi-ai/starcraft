from sc2reader.events import Event


class CoOpEvent:
    PLAYER_EVENT = "PlayerEvent"
    GAME_EVENT = "GameEvent"
    UNITBORN_EVENT = "UnitBornEvent"
    def __init__(self, events:list[Event]):
        self.events = events
        self.event_types = self.get_event_types()
        self.players_events = self.arrange_events()

    def get_event_types(self)->dict[str, set[str]]:
        game_events = set()
        player_events = set()
        for event in self.events:
            value = getattr(event, "control_pid", None)
            if value == None:
                game_events.add(event.name)
            else:
                player_events.add(event.name)

        types = dict()
        types[self.GAME_EVENT] = game_events
        types[self.PLAYER_EVENT] = player_events

        return types

    def arrange_events(self)->dict[int, list]:
        events = {}
        for event in self.events:
            if event.name in self.event_types[self.PLAYER_EVENT]:
                id = event.control_pid
                event_list = []
                if id in events:
                    event_list = events[id]
                event_list.append(event)
                events[id] = event_list

        return events
    def get_unit_born_events(self):
        events = list[Event]()
        for event in self.events:
            if event.name == self.UNITBORN_EVENT:
                events.append(event)

        return events

    def get_unit_born_events_for_player(self, id:int)->list[Event]:
        events = list[Event]()
        for event in self.players_events[id]:
            if event.name == self.UNITBORN_EVENT:
                events.append(event)

        return events