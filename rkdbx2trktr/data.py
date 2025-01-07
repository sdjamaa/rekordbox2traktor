import urllib
import logging
from pathlib import Path

from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.wave import WAVE

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('audioDataLogger')


def load_mp3_file(file_path: str) -> MP3:
    return MP3(file_path)


def load_wave_file(file_path: str) -> WAVE:
    return WAVE(file_path)


def load_flac_file(file_path: str) -> FLAC:
    return FLAC(file_path)


def get_file_size(file_path: str) -> int:
    return Path(file_path).stat().st_size


def audio_analyzer_class(track_path: str):
    track_path = track_path.replace("file://localhost", "")
    track_path = urllib.parse.unquote(track_path)

    logger.debug(f"Importing {track_path}")

    audio_file = None

    if track_path.lower().endswith("mp3"):
        audio_file = AudioFile("MP3", track_path)

    if track_path.lower().endswith("flac"):
        audio_file = AudioFile("FLAC", track_path)

    if track_path.lower().endswith("wav"):
        audio_file = AudioFile("WAVE", track_path)

    if audio_file is None:
        extension = track_path.split(".")[-1]
        raise AudioFileTypeNotKnownException(f"File with extension '{extension}' not known.")

    return audio_file


class AudioFile:
    audio_type: MP3 | FLAC | WAVE

    artist = ""
    title = ""
    bitrate: int
    filesize: int

    def __init__(self, audio_type: str, track_path: str):
        try:
            match audio_type:
                case "MP3" | "WAVE":
                    audio_file = load_mp3_file(track_path) if audio_type == "MP3" else load_wave_file(track_path)
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
