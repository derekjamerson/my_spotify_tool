from random import randint

from libraries.factories import LibraryFactory
from testing import BaseTestCase
from tracks.factories import TrackFactory


class TestLibrary(BaseTestCase):
    def setUp(self):
        self.library = LibraryFactory()

    def test_duration_string(self):
        durations = [
            randint(1, 59999),
            randint(60000, 3599999),
            randint(3600000, 9999999),
            randint(86401000, 99999999),
        ]
        for actual_ms in durations:
            self.library.tracks.set(TrackFactory.create_batch(3, duration_ms=actual_ms))
            actual_string = self.library.total_duration
            days = int(actual_ms * 3 / (1000 * 60 * 60 * 24))
            hours = int(actual_ms * 3 / (1000 * 60 * 60)) % 24
            minutes = int(actual_ms * 3 / (1000 * 60)) % 60
            seconds = int(actual_ms * 3 / 1000) % 60
            if days:
                expected_string = f'{days:03d}:{hours:02d}:{minutes:02d}:{seconds:02d}'
            elif hours:
                expected_string = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
            elif minutes:
                expected_string = f'{minutes:02d}:{seconds:02d}'
            else:
                expected_string = str(seconds)
            self.assertEqual(expected_string, actual_string)
