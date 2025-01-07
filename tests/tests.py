import unittest
import os
from unittest.mock import Mock, patch
import xml.etree.ElementTree as ET

from rkdbx2trktr import parse_rekordbox, audio_analyzer_class
from rkdbx2trktr.utils import flatten_playlists


class TestRekordboxToTraktorConversion(unittest.TestCase):

    def test_small_rekordbox_xml(self):
        regular_xml_file = os.path.join(os.path.dirname(__file__), 'testfiles/regular_small.xml')
        result = parse_rekordbox(regular_xml_file)
        self.assertEqual(result, {'chill': ["file://localhost/Volumes/Tracks/Herbert%20-%20I%20Hadn%27t%20Known%20(I%20Only%20Heard).mp3"]})

    def test_nested_playlists_rekordbox_xml(self):
        regular_nested_playlists = os.path.join(os.path.dirname(__file__), 'testfiles/regular_nested_playlists.xml')
        result = parse_rekordbox(regular_nested_playlists)
        self.assertEqual(result, {'Breaks': ["file://localhost/Volumes/Tracks/Herbert%20-%20I%20Hadn%27t%20Known%20(I%20Only%20Heard).mp3"]})

    def test_flatten_playlists_node(self):
        nested_playlists = os.path.join(os.path.dirname(__file__), 'testfiles/flatten_playlists.xml')
        tree = ET.parse(nested_playlists)
        playlists = tree.find('PLAYLISTS/NODE')
        result = flatten_playlists(playlists)
        count = 0
        for res in result:
            count += 1
            self.assertEqual(res.tag, "NODE")
        self.assertEqual(count, 2)

    @patch("mutagen.MP3")
    def test_audiofile_mp3(self, mock_mp3):
        mock_mp3_object = { 'artist' : "aama", 'title': "super mix"}
        mock_mp3.return_value(mock_mp3_object)
        audio_analyzer_class("/Users/aama.mp3")


if __name__ == '__main__':
    unittest.main()
