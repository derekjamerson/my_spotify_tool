from libraries.factories import LibraryFactory
from playlists.models import Playlist
from playlists.utils import PlaylistUtils
from testing.base import BaseTestCase
from users.factories import CustomUserFactory


class PlaylistUtilsTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.playlist_utils = PlaylistUtils()
        self.user = CustomUserFactory()
        self.library = LibraryFactory(user=self.user)

    def test_create_random(self):
        playlist = self.playlist_utils.create_random(self.user)
        self.assertCountEqual(playlist.tracks, list(self.library.tracks.all()))

    def test_create_playlist_by_artist_tracks(self):
        test_track = self.library.tracks.all()[0]
        test_artist = test_track.artists.all()[0]
        playlist = self.playlist_utils.create_by_artists(
            user=self.user, artists=[test_artist], name='test_playlist'
        )
        self.assertEqual(playlist.tracks, [test_track])
