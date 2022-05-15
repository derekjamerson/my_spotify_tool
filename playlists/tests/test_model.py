from playlists.factories import PlaylistFactory
from testing.base import BaseTestCase


class TestPlaylist(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.playlist = PlaylistFactory().playlist

    def test_track_uris(self):
        result = list(self.playlist.track_uris)
        self.assertEqual(len(result), 2)
