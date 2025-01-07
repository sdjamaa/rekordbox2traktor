import unittest
from unittest.mock import Mock, patch, PropertyMock

from rkdbx2trktr import audio_analyzer_class


class TestAudioFileLoading(unittest.TestCase):

    @patch("data.load_mp3_file")
    @patch("data.get_file_size")
    def test_audiofile_mp3(self, mock_file_size, mock_mp3):
        type(mock_mp3.return_value).tags = PropertyMock(return_value={
            'TPE1': Mock(text=["aama"]),
            'TIT2': Mock(text=["super mix"])
        })
        type(mock_mp3.return_value).info = PropertyMock(return_value=Mock(bitrate=99))
        mock_file_size.return_value = 10000

        file = audio_analyzer_class("/Users/aama.mp3")

        self.assertEqual("aama", file.artist)
        self.assertEqual("super mix", file.title)
        self.assertEqual(99, file.bitrate)
        self.assertEqual(10000, file.filesize)

    @patch("data.load_mp3_file")
    @patch("data.get_file_size")
    def test_audiofile_mp3_uppercase(self, mock_file_size, mock_mp3):
        type(mock_mp3.return_value).tags = PropertyMock(return_value={
            'TPE1': Mock(text=["aama"]),
            'TIT2': Mock(text=["super mix"])
        })
        type(mock_mp3.return_value).info = PropertyMock(return_value=Mock(bitrate=99))
        mock_file_size.return_value = 10000

        file = audio_analyzer_class("/Users/aama.MP3")

        self.assertEqual("aama", file.artist)
        self.assertEqual("super mix", file.title)
        self.assertEqual(99, file.bitrate)
        self.assertEqual(10000, file.filesize)


    @patch("data.load_wave_file")
    @patch("data.get_file_size")
    def test_audiofile_wave(self, mock_file_size, mock_wave):
        type(mock_wave.return_value).tags = PropertyMock(return_value={
            'TPE1': Mock(text=["aama"]),
            'TIT2': Mock(text=["super mix"])
        })
        type(mock_wave.return_value).info = PropertyMock(return_value=Mock(bitrate=99))
        mock_file_size.return_value = 10000

        file = audio_analyzer_class("/Users/aama.wav")

        self.assertEqual("aama", file.artist)
        self.assertEqual("super mix", file.title)
        self.assertEqual(99, file.bitrate)
        self.assertEqual(10000, file.filesize)

    @patch("data.load_flac_file")
    @patch("data.get_file_size")
    def test_audiofile_flac(self, mock_file_size, mock_flac):
        type(mock_flac.return_value).tags = PropertyMock(return_value={
            'artist': ["aama"],
            'title': ["super mix"]
        })
        type(mock_flac.return_value).info = PropertyMock(return_value=Mock(bitrate=99))
        mock_file_size.return_value = 10000

        file = audio_analyzer_class("/Users/aama.flac")

        self.assertEqual("aama", file.artist)
        self.assertEqual("super mix", file.title)
        self.assertEqual(99, file.bitrate)
        self.assertEqual(10000, file.filesize)