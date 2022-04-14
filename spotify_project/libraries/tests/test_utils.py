from libraries.factories import LibraryFactory
from libraries.utils import LibraryUtils
from testing import BaseTestCase
from users.factories import CustomUserFactory


class LibraryUtilsTestCase(BaseTestCase):
    def setUp(self):
        self.library_utils = LibraryUtils()
        self.user = CustomUserFactory()
        self.library = LibraryFactory(user=self.user)

    def test_add_library_to_db(self):
        self.add_dummy_objects_to_db()
        self.library_utils.add_library_to_db(self.dummy_library_data, self.user)
        self.assertEqual(len(self.user.library.tracks.all()), 3)
        self.assertEqual(len(self.user.library.artists.all()), 5)

    def test_get_all_artist_pks(self):
        artist_pks = self.library_utils.get_all_artist_pks(self.dummy_library_data)
        actual_pks = sorted(artist_pks)
        expected_pks = sorted(
            [
                artist['id']
                for track in self.dummy_library_data
                for artist in track['artists']
            ]
        )
        self.assertEqual(actual_pks, expected_pks)
