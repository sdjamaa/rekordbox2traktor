import uuid
from functools import reduce
from datetime import date
import urllib.parse

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

from data import audio_analyzer_class


def format_path_for_traktor(track: str):
    if track.startswith("/Volumes"):
        formatted_track_path = track.replace("/Volumes/", "")
    elif track.startswith("/"):
        formatted_track_path = "Macintosh HD/" + track[1: len(track)]
    formatted_track_path = formatted_track_path.replace("/", "/:")
    formatted_track_path = urllib.parse.unquote(formatted_track_path)
    return formatted_track_path


def write_collection_entries(root: Element, p: dict):
    total_tracks = reduce(lambda x, y: x + y, [len(tracks) for tracks in p.values()])
    collection = ET.SubElement(root, "COLLECTION", ENTRIES=str(total_tracks))
    all_tracks = [track for tracks in p.values() for track in tracks]
    for track in all_tracks:
        audio_file = audio_analyzer_class(track)

        strdate = date.today().strftime("%Y/%-m/%-d")
        entry = ET.SubElement(collection, "ENTRY",
                              MODIFIED_DATE=strdate,
                              MODIFIED_TIME="5189",  # ???? wtf is that
                              TITLE=audio_file.title,
                              ARTIST=audio_file.artist)
        formatted_track_path = format_path_for_traktor(track)
        split_path = formatted_track_path.split("/:")
        dir_name = "/:" + "/:".join(split_path[1:len(split_path) - 1])
        if len(dir_name) > 2:
            dir_name = dir_name + "/:"
        file_name = split_path[-1]
        volume_name = split_path[0]

        ET.SubElement(entry, "LOCATION", DIR=dir_name, FILE=file_name, VOLUME=volume_name, VOLUMEID=volume_name)
        ET.SubElement(entry, "MODIFICATION_INFO", AUTHOR_TYPE="importer")
        ET.SubElement(entry, "INFO", BITRATE=str(audio_file.bitrate), IMPORT_DATE=strdate, FILESIZE=str(int(audio_file.filesize / 1000)))


def write_playlists(root: Element, p: dict):
    playlists = ET.SubElement(root, "PLAYLISTS")
    node = ET.SubElement(playlists, "NODE", TYPE="FOLDER", NAME="$ROOT")

    playlist_count = len(p)
    subnodes = ET.SubElement(node, "SUBNODES", COUNT=str(playlist_count))

    for playlist_name, tracks in p.items():
        n_playlist = ET.SubElement(subnodes, "NODE", TYPE="PLAYLIST", NAME=playlist_name)
        playlist = ET.SubElement(n_playlist, "PLAYLIST", ENTRIES=str(len(tracks)), TYPE="LIST", UUID=uuid.uuid4().hex)
        for track in tracks:
            formatted_track_path = format_path_for_traktor(track)
            entry = ET.SubElement(playlist, "ENTRY")
            ET.SubElement(entry, "PRIMARYKEY", TYPE="TRACK", KEY=formatted_track_path)


def generate_traktor_playlist(p: dict, traktor_coll_path: str):
    root = ET.Element("NML", VERSION="19")
    ET.SubElement(root, "HEAD", COMPANY="www.native-instruments.com", PROGRAM="Traktor")
    write_collection_entries(root, p)

    ET.SubElement(root, "SETS", ENTRIES="0")

    write_playlists(root, p)

    ET.SubElement(root, "INDEXING")

    tree = ET.ElementTree(root)
    tree.write(traktor_coll_path, encoding="utf-8")
