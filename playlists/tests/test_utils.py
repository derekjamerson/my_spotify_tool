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

    def test_create_playlist_by_artist_tracks(self):
        test_track = self.library.tracks.all()[0]
        test_artist = test_track.artists.all()[0]
        playlist = self.playlist_utils.create_by_artists(self.user, [test_artist])
        self.assertEqual(playlist.tracks, [test_track])

    def test_create_playlist_by_artist_text_1(self):
        test_tracks = self.library.tracks.all()[0]
        test_artists = test_tracks.artists.all()[0]
        playlist = self.playlist_utils.name_playlist_by_artist([test_artists])
        expected = test_artists.name
        self.assertEqual(playlist.name, expected)

    def test_create_playlist_by_artist_text_2(self):
        test_tracks = self.library.tracks.all()[:2]
        test_artists = []
        for track in test_tracks:
            test_artists.append(track.artists.all()[0])
        playlist = self.playlist_utils.name_playlist_by_artist(test_artists)
        expected = f'{test_artists[0].name} and {test_artists[1].name}'
        self.assertEqual(playlist.name, expected)

    def test_create_playlist_by_artist_text_4(self):
        test_tracks = self.library.tracks.all()[:2]
        test_artists = []
        for track in test_tracks:
            test_artists.append(track.artists.all()[0])
            test_artists.append(track.artists.all()[1])
        playlist = self.playlist_utils.name_playlist_by_artist(test_artists)
        expected = f'{test_artists[0].name} and Friends'
        self.assertEqual(playlist.name, expected)
