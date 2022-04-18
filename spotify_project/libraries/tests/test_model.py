from random import randint

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

    def test_duration_string(self):
        num_tracks = 3
        durations = [
            randint(1, 59999 // num_tracks),
            randint(60000 // num_tracks, 3599999 // num_tracks),
            randint(3600000 // num_tracks, 9999999 // num_tracks),
            randint(86401000 // num_tracks, 99999999 // num_tracks),
        ]
        for actual_ms in durations:
            self.library.tracks.set(
                TrackFactory.create_batch(num_tracks, duration_ms=actual_ms)
            )
            actual_string = self.library.total_duration
            days = int(actual_ms * num_tracks / (1000 * 60 * 60 * 24))
            hours = int(actual_ms * num_tracks / (1000 * 60 * 60)) % 24
            minutes = int(actual_ms * num_tracks / (1000 * 60)) % 60
            seconds = int(actual_ms * num_tracks / 1000) % 60
            if days:
                expected_string = f'{days:03d}:{hours:02d}:{minutes:02d}:{seconds:02d}'
            elif hours:
                expected_string = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
            elif minutes:
                expected_string = f'{minutes:02d}:{seconds:02d}'
            else:
                expected_string = str(seconds)
            self.assertEqual(expected_string, actual_string)
