from mpyq import MPQArchive
from s2protocol import versions

class ReplayFactory:
    @staticmethod
    def replay_from_s2protocol(replay_path: str):
        """
        Load tracker events from a replay.
        """

        archive = MPQArchive(replay_path)

        header = versions.latest().decode_replay_header(
            archive.header['user_data_header']['content']
        )

        base_build = header["m_version"]["m_baseBuild"]

        protocol = versions.build(base_build)

        contents = archive.read_file("replay.tracker.events")

        tracker_events = protocol.decode_replay_tracker_events(contents)

        return tracker_events