from testing import BaseTestCase
from tracks.factories import TrackFactory


class TestTrack(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.track = TrackFactory()
