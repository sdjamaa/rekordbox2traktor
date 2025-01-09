import sys

from rekordbox import parse_rekordbox
from traktor import generate_traktor_playlist

# TODO: add setup.py?
# TODO: make it pypi package?
# TODO: create CI/CD check to generate github tickets from TODO comments
# TODO: add checks based on attributes (e.g. Count="111")
# TODO: add tool to check validity of tags
if __name__ == "__main__":
    # TODO: use proper cmd line parser with options
    rekordbox_coll_path = sys.argv[1]
    traktor_coll_path = sys.argv[2]
    playlists = parse_rekordbox(rekordbox_coll_path)
    generate_traktor_playlist(playlists, traktor_coll_path)
