from operator import itemgetter

from albums.factories import AlbumFactory
from albums.models import Album
from albums.utils import AlbumUtils
from artists.factories import ArtistFactory
from testing import BaseTestCase


class AlbumUtilsTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.album_utils = AlbumUtils()
        self.artist = ArtistFactory()
        self.album = AlbumFactory(artists=[self.artist])
        # not included
        AlbumFactory(artists=[ArtistFactory()])

    def test_add_albums_to_db(self):
        with self.assert_num_objects_created({Album: 3}):
            self.album_utils.add_albums_to_db(self.dummy_library_data)

    def test_get_all_albums(self):
        actual_albums = list(self.album_utils.get_all_albums(self.dummy_library_data))
        expected_albums = [track['album'] for track in self.dummy_library_data]
        for count, album in enumerate(actual_albums):
            self.assertEqual(album.pk, expected_albums[count]['id'])
            self.assertEqual(album.name, expected_albums[count]['name'])

    def test_get_new_albums(self):
        unsaved_albums = AlbumFactory.build_batch(2)
        unsaved_albums.append(self.album)
        new_albums = list(self.album_utils.get_new_albums(unsaved_albums))
        self.assertEqual(len(new_albums), 2)

    def test_add_album_artist_m2m(self):
        self.add_dummy_objects_to_db()
        with self.assert_num_objects_created({Album.artists.through: 5}):
            self.album_utils.add_album_artist_m2m(self.dummy_library_data)

    def test_get_all_album_artist_throughs(self):
        actual_throughs = list(
            self.album_utils.get_all_album_artist_throughs(self.dummy_library_data)
        )
        expected_throughs_with_duplicates = []
        for track in self.dummy_library_data:
            for artist in track['album']['artists']:
                expected_throughs_with_duplicates.append(
                    (track['album']['id'], artist['id'])
                )
        expected_throughs = sorted(
            set(expected_throughs_with_duplicates), key=itemgetter(0, 1)
        )
        for count, through in enumerate(sorted(actual_throughs, key=itemgetter(0, 1))):
            self.assertEqual(through, expected_throughs[count])

    def test_new_album_artist_throughs(self):
        new_album = AlbumFactory()
        unsaved_throughs = [
            (new_album.pk, self.artist.pk),
            (self.album.pk, self.artist.pk),
        ]
        new_throughs = list(
            self.album_utils.get_new_album_artist_throughs(unsaved_throughs)
        )
        self.assertEqual(len(new_throughs), 1)
