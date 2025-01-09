import xml.etree.ElementTree as ET

from utils import flatten_playlists, clean_path


def parse_rekordbox(rekordbox_coll_path: str) -> dict:
    all_playlists = {}

    tree = ET.parse(rekordbox_coll_path)
    tracks = tree.find('COLLECTION')
    all_tracks = {}
    for track in tracks:
        track_id = track.attrib['TrackID']
        track_path = track.attrib['Location']
        # TODO: weird v4/catalog path from Rekordbox internal library I guess
        if "catalog" in track_path:
            continue
        cleaned_path = clean_path(track_path)
        all_tracks.update({track_id: cleaned_path})

    playlists = tree.find('PLAYLISTS/NODE')
    for playlist in flatten_playlists(playlists):
        playlist_name = playlist.attrib["Name"]
        playlist_tracks = []
        for n in playlist:
            key = n.attrib["Key"]
            if key not in all_tracks:
                continue
            playlist_tracks.append(all_tracks[key])
        all_playlists.update({playlist_name: playlist_tracks})

    return all_playlists
