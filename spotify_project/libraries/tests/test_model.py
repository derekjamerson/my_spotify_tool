from artists.factories import ArtistFactory
from libraries.factories import LibraryFactory
from testing import BaseTestCase
from tracks.factories import TrackFactory


class TestLibrary(BaseTestCase):
    def setUp(self):
        self.artists = ArtistFactory.create_batch(11)
        self.tracks = TrackFactory.create_batch(3, artists=self.artists)
        self.tracks += TrackFactory.create_batch(3, artists=[self.artists[0]])
        self.library = LibraryFactory(tracks=self.tracks, artists=self.artists)

    def test_top_artists(self):
        result = self.library.top_artists
        self.assertEqual(len(result), 10)
        for artist, count in result.items():
            if artist == self.artists[0]:
                self.assertEqual(count, 6)
            else:
                self.assertEqual(count, 3)
