from artists.factories import ArtistFactory
from artists.models import Artist
from artists.utils import ArtistUtils
from testing import BaseTestCase


class AlbumUtilsTestCase(BaseTestCase):
    def setUp(self):
        self.artist_utils = ArtistUtils()
        self.artist = ArtistFactory()
        # not included
        ArtistFactory()

    def test_add_artists_to_db(self):
        with self.assert_num_objects_created({Artist: 5}):
            self.artist_utils.add_artists_to_db(self.dummy_library_data)

    def test_get_all_artists(self):
        actual_artists = sorted(
            list(self.artist_utils.get_all_artists(self.dummy_library_data)),
            key=lambda x: x.pk,
        )
        artists_from_tracks = [
            artist for track in self.dummy_library_data for artist in track['artists']
        ]
        artists_from_albums = [
            artist
            for track in self.dummy_library_data
            for artist in track['album']['artists']
        ]
        expected_artists = sorted(
            artists_from_tracks + artists_from_albums, key=lambda x: x['id']
        )
        for count, artist in enumerate(actual_artists):
            self.assertEqual(artist.pk, expected_artists[count]['id'])
            self.assertEqual(artist.name, expected_artists[count]['name'])

    def test_get_new_albums(self):
        unsaved_artists = ArtistFactory.build_batch(2)
        unsaved_artists.append(self.artist)
        new_artists = list(self.artist_utils.get_new_artists(unsaved_artists))
        self.assertEqual(len(new_artists), 2)
