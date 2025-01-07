import sys
import uuid
from functools import reduce
from datetime import date
import urllib.parse

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

from rekordbox import parse_rekordbox
from data import audio_analyzer_class


# TODO: add setup.py?
# TODO: make it pypi package?
# TODO: create CI/CD check to generate github tickets from TODO comments
# TODO: add checks based on attributes (e.g. Count="111")
# TODO: add tool to check validity of tags
def format_path_for_traktor(track: str):
    if track.startswith("file://localhost/Volumes"):
        formatted_track_path = track.replace("file://localhost/Volumes/", "")
    else:
        formatted_track_path = track.replace("file://localhost/", "Macintosh HD/")
    formatted_track_path = formatted_track_path.replace("/", "/:")
    formatted_track_path = urllib.parse.unquote(formatted_track_path)
    return formatted_track_path


def write_collection_entries(root: Element, p: dict):
    total_tracks = reduce(lambda x, y: x + y, [len(tracks) for tracks in p.values()])
    collection = ET.SubElement(root, "COLLECTION", entries=str(total_tracks))
    all_tracks = [track for tracks in p.values() for track in tracks]
    for track in all_tracks:
        # track_path = track.replace("file://localhost", "")
        # track_path = urllib.parse.unquote(track_path)
        audio_file = audio_analyzer_class(track)

        strdate = date.today().strftime("%d/%m/%y")
        entry = ET.SubElement(collection, "ENTRY",
                              modified_date=strdate,
                              modified_time="5189",  # ???? wtf is that
                              title=audio_file.title,
                              artist=audio_file.artist)
        formatted_track_path = format_path_for_traktor(track)
        dir_name = "/".join(formatted_track_path[1:len(formatted_track_path) - 1])
        file_name = formatted_track_path.split("/")[-1]
        volume_name = formatted_track_path.split("/")[0]
        ET.SubElement(entry, "LOCATION", dir=dir_name, file=file_name, volume=volume_name, volumeid=volume_name)
        ET.SubElement(entry, "MODIFICATION_INFO", author_type="importer")
        ET.SubElement(entry, "INFO", bitrate=str(audio_file.bitrate), IMPORT_DATE=strdate, filesize=str(audio_file.filesize))


def write_playlists(root: Element, p: dict):
    playlists = ET.SubElement(root, "PLAYLISTS")
    node = ET.SubElement(playlists, "NODE", type="folder", name="$ROOT")

    playlist_count = len(p)
    subnodes = ET.SubElement(node, "SUBNODES", count=str(playlist_count))

    for playlist_name, tracks in p.items():
        n_playlist = ET.SubElement(subnodes, "NODE", type="PLAYLIST", name=playlist_name)
        playlist = ET.SubElement(n_playlist, "PLAYLIST", entries=str(len(tracks)), type="list", uuid=uuid.uuid4().hex)
        for track in tracks:
            formatted_track_path = format_path_for_traktor(track)
            entry = ET.SubElement(playlist, "ENTRY")
            ET.SubElement(entry, "PRIMARYKEY", type="track", KEY=formatted_track_path)


def generate_traktor_playlist(p: dict, traktor_coll_path: str):
    root = ET.Element("NML")
    doc = ET.SubElement(root, "HEAD", company="www.native-instruments.com", program="Traktor")

    write_collection_entries(root, p)
    write_playlists(root, p)

    tree = ET.ElementTree(root)
    tree.write(traktor_coll_path)


if __name__ == "__main__":
    # TODO: use proper cmd line parser with options
    rekordbox_coll_path = sys.argv[1]
    traktor_coll_path = sys.argv[2]
    playlists = parse_rekordbox(rekordbox_coll_path)
    generate_traktor_playlist(playlists, traktor_coll_path)
