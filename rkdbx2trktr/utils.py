import urllib
from typing import Optional

from xml.etree.ElementTree import Element


def clean_path(path: str) -> str:
    # TODO: this should be specialized by software in input (Rekordbox uses file://, etc...)
    track_path = path.replace("file://localhost", "")
    track_path = urllib.parse.unquote(track_path)
    return track_path


def flatten_playlists(playlists_node: Optional[Element]):
    for node in playlists_node:
        nested_nodes = [x for x in node if x.tag == "NODE"]
        if len(nested_nodes) > 0:
            for n in node:
                yield n
        else:
            yield node
