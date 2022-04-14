from operator import itemgetter

from artists.factories import ArtistFactory
from testing import BaseTestCase
from tracks.factories import TrackFactory
from tracks.models import Track
from tracks.utils import TrackUtils


class TrackUtilsTestCase(BaseTestCase):
    def setUp(self):
        self.track_utils = TrackUtils()
        self.artists = [ArtistFactory()]
        self.track = TrackFactory(artists=self.artists)
        # not included
        TrackFactory(artists=[ArtistFactory()])

    def test_add_tracks_to_db(self):
        self.add_dummy_objects_to_db(add_tracks=False)
        with self.assert_num_objects_created({Track: 3}):
            self.track_utils.add_tracks_to_db(self.dummy_library_data)

    def test_get_all_tracks(self):
        actual_tracks = list(self.track_utils.get_all_tracks(self.dummy_library_data))
        expected_tracks = [track for track in self.dummy_library_data]
        for count, track in enumerate(actual_tracks):
            self.assertEqual(track.pk, expected_tracks[count]['id'])
            self.assertEqual(track.name, expected_tracks[count]['name'])

    def test_get_new_tracks(self):
        unsaved_tracks = TrackFactory.build_batch(2)
        unsaved_tracks.append(self.track)
        new_tracks = list(self.track_utils.get_new_tracks(unsaved_tracks))
        self.assertEqual(len(new_tracks), 2)

    def test_add_track_artist_m2m(self):
        self.add_dummy_objects_to_db()
        with self.assert_num_objects_created({Track.artists.through: 7}):
            self.track_utils.add_track_artist_m2m(self.dummy_library_data)

    def test_get_all_track_artist_throughs(self):
        actual_throughs = list(
            self.track_utils.get_all_track_artist_throughs(self.dummy_library_data)
        )
        expected_throughs_with_duplicates = []
        for track in self.dummy_library_data:
            for artist in track['artists']:
                expected_throughs_with_duplicates.append((track['id'], artist['id']))
        expected_throughs = sorted(
            set(expected_throughs_with_duplicates), key=itemgetter(0, 1)
        )
        for count, through in enumerate(sorted(actual_throughs, key=itemgetter(0, 1))):
            self.assertEqual(through, expected_throughs[count])

    def test_new_track_artist_throughs(self):
        new_track = TrackFactory()
        unsaved_throughs = [
            (new_track.pk, self.artists[0].pk),
            (new_track.pk, self.artists[0].pk),
            (self.track.pk, self.artists[0].pk),
        ]
        new_throughs = list(
            self.track_utils.get_new_track_artist_throughs(unsaved_throughs)
        )
        self.assertEqual(len(new_throughs), 2)
