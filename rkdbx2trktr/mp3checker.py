import sys
import logging

from mutagen import MutagenError

from rekordbox import parse_rekordbox
from data import audio_analyzer_class, AudioFileTagException, AudioFileMissingTagException
from utils import clean_path

# TODO: better logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('mp3checker')


# TODO: add stats for playlists (e.g. # of errors per playlist, categorization...)
def check_missing_tags(library: dict):
    for playlist, tracks in library.items():
        # TODO: remove those horrible print with proper logging
        print("----------------------------------------")
        print(playlist)
        for track in tracks:
            try:
                clean_track_path = clean_path(track)
                audio_analyzer_class(clean_track_path)
                print(clean_track_path)
            except AudioFileTagException as e:
                logging.error(f"Can't parse tags for {clean_track_path}")
            except AudioFileMissingTagException as e:
                logging.error(f"Missing tags for {clean_track_path}")
                logging.error(e)
            except MutagenError as e:
                logging.error("mutagen internal error.")
                logging.error(e)


if __name__ == "__main__":
    # TODO: use proper cmd line parser with options
    # TODO: should have the choice between whatever software (e.g. rekordbox, traktor, serato...)
    rekordbox_coll_path = sys.argv[1]
    rekordbox_library = parse_rekordbox(rekordbox_coll_path)
    check_missing_tags(rekordbox_library)
