import random

from testing import BaseTestCase
from tracks.factories import TrackFactory


class TestTrack(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.track = TrackFactory()

    def test_duration_string(self):
        durations = [
            random.randint(1, 59999),
            random.randint(60000, 3599999),
            random.randint(3600000, 9999999),
        ]
        for actual_ms in durations:
            self.track.duration_ms = actual_ms
            actual_string = self.track.duration_string
            hours = int(actual_ms / (1000 * 60 * 60)) % 24
            minutes = int(actual_ms / (1000 * 60)) % 60
            seconds = int(actual_ms / 1000) % 60
            if hours:
                expected = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
            elif minutes:
                expected = f'{minutes:02d}:{seconds:02d}'
            else:
                expected = str(seconds)
            self.assertEqual(expected, actual_string)
