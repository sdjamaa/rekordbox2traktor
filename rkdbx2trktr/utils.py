from typing import Optional

from xml.etree.ElementTree import Element


def flatten_playlists(playlists_node: Optional[Element]):
    for node in playlists_node:
        nested_nodes = [x for x in node if x.tag == "NODE"]
        if len(nested_nodes) > 0:
            for n in node:
                yield n
        else:
            yield node
