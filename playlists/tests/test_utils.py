from libraries.factories import LibraryFactory
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
