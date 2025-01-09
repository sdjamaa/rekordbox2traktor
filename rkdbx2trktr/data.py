import urllib
import logging
from pathlib import Path

from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.wave import WAVE
from mutagen.aiff import AIFF
from mutagen.mp4 import MP4

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('audioDataLogger')


def load_mp3_file(file_path: str) -> MP3:
    return MP3(file_path)


def load_wave_file(file_path: str) -> WAVE:
    return WAVE(file_path)


def load_flac_file(file_path: str) -> FLAC:
    return FLAC(file_path)


def load_aiff_file(file_path: str) -> AIFF:
    return AIFF(file_path)


def load_mp4_file(file_path: str) -> MP4:
    return MP4(file_path)


def get_file_size(file_path: str) -> int:
    return Path(file_path).stat().st_size


def audio_analyzer_class(track_path: str):
    """Creates a AudioFile for a given audio file type and reads ID3 tags.
    Important: path should be formatted already for Unix/OSX (starts with '/').
    Please use clean_path method to decode from URL string and remove useless prefixes.

    Raises exceptions if path is wrong, audio file or tags can't be read...
    """
    logger.debug(f"Importing {track_path}")

    # TODO: add more checks for paths (e.g. depending on OS)
    if track_path == "" or track_path is None:
        raise AudioFilePathDoesNotExistException("Path cannot be empty...")

    audio_file = None

    if track_path.lower().endswith("mp3"):
        audio_file = AudioFile("MP3", track_path)

    if track_path.lower().endswith("flac"):
        audio_file = AudioFile("FLAC", track_path)

    if track_path.lower().endswith("wav"):
        audio_file = AudioFile("WAVE", track_path)

    if track_path.lower().endswith("aiff"):
        audio_file = AudioFile("AIFF", track_path)

    if track_path.lower().endswith("m4a") or track_path.lower().endswith("mp4"):
        audio_file = AudioFile("MP4", track_path)

    if audio_file is None:
        extension = track_path.split(".")[-1]
        raise AudioFileTypeNotKnownException(f"File with extension '{extension}' not known.")

    return audio_file


class AudioFile:
    audio_type: MP3 | FLAC | WAVE | AIFF | MP4

    artist = ""
    title = ""
    bitrate: int
    filesize: int

    def __init__(self, audio_type: str, track_path: str):
        try:
            match audio_type:
                case "MP3" | "WAVE" | "AIFF":
                    if audio_type == "MP3":
                        audio_file = load_mp3_file(track_path)
                    elif audio_type == "WAVE":
                        audio_file = load_wave_file(track_path)
                    elif audio_type == "AIFF":
                        audio_file = load_aiff_file(track_path)
                    if audio_file == {}:
                        raise AudioFileTagException("Can't get tracks from mutagen package.")
                    self.artist = audio_file.tags['TPE1'].text[0]
                    self.title = audio_file.tags['TIT2'].text[0]
                case "FLAC":
                    audio_file = load_flac_file(track_path)
                    if audio_file == {}:
                        raise AudioFileTagException("Can't get tracks from mutagen package.")
                    self.artist = audio_file.tags['artist'][0]
                    self.title = audio_file.tags['title'][0]
                case "MP4":
                    audio_file = load_mp4_file(track_path)
                    if audio_file == {}:
                        raise AudioFileTagException("Can't get tracks from mutagen package.")
                    self.artist = audio_file.tags['©ART'][0]
                    self.title = audio_file.tags['©nam'][0]

            self.bitrate = audio_file.info.bitrate
            self.filesize = get_file_size(track_path)
        except KeyError as ke:
            raise AudioFileMissingTagException(f"Key missing: {ke}")


class AudioFileTagException(Exception):
    def __init__(self, message):
        super().__init__(message)


class AudioFileMissingTagException(Exception):
    def __init__(self, message):
        super().__init__(message)


class AudioFileTypeNotKnownException(Exception):
    def __init__(self, message):
        super().__init__(message)


class AudioFilePathDoesNotExistException(Exception):
    def __init__(self, message):
        super().__init__(message)
