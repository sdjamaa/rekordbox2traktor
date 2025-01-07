import sys
import logging

from rekordbox import parse_rekordbox
from data import audio_analyzer_class, AudioFileTagException, AudioFileMissingTagException


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('mp3checker')


def check_missing_tags(library: dict):
    for tracks in library.values():
        for track in tracks:
            try:
                audio_analyzer_class(track)
            except AudioFileTagException as e:
                logging.error(f"Can't parse tags for {track}")
            except AudioFileMissingTagException as e:
                logging.error(f"Missing tags for {track}")
                logging.error(e)


if __name__ == "__main__":
    # TODO: use proper cmd line parser with options
    # TODO: should have the choice between whatever software (e.g. rekordbox, traktor, serato...)
    rekordbox_coll_path = sys.argv[1]
    rekordbox_library = parse_rekordbox(rekordbox_coll_path)
    check_missing_tags(rekordbox_library)
