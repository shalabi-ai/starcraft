from replay.analyser import ReplayAnalyser
from replay.analyser import ReplayAnalyser
from replay.processor import ReplayProcessor
from replay.replay import CoOpReplay
import sc2reader

class AnalyserFactory:
    @staticmethod
    def create_analyser(path: str)->ReplayAnalyser:
        replay1 = sc2reader.load_replay(path)

        coopReplay = CoOpReplay(replay1)
        players = coopReplay.getPlayerMap()

        processor = ReplayProcessor(replay1)
        kills, kill_events = processor.process_replay()

        analyser = ReplayAnalyser(players, kills, kill_events)
        return analyser