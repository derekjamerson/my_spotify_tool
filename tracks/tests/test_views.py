from django.urls import reverse

from testing import BaseTestCase
from tracks.factories import TrackFactory


class TrackInfoTestCase(BaseTestCase):
    @property
    def url(self):
        return reverse(
            'tracks:track_info',
            kwargs={'track_id': self.track.spotify_id},
        )

    def setUp(self):
        super().setUp()
        self.track = TrackFactory()

    def test_GET_returns_200(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)

    def test_track_name_present(self):
        r = self.client.get(self.url)
        actual = self.css_select_get_text(r, 'dl.properties dd#track-name')[0]
        expected = self.track.name
        self.assertEqual(actual, expected)

    def test_album_name_present(self):
        r = self.client.get(self.url)
        actual = self.css_select_get_text(r, 'dl.properties dd#track-album')[0]
        expected = self.track.album.name
        self.assertEqual(actual, expected)

    def test_track_id_present(self):
        r = self.client.get(self.url)
        actual = self.css_select_get_text(r, 'dl.properties dd#track-id')[0]
        expected = self.track.spotify_id
        self.assertEqual(actual, expected)

    def test_duration_present(self):
        r = self.client.get(self.url)
        actual = self.css_select_get_text(r, 'dl.properties dd#duration')[0]
        dur_min, dur_sec = divmod(self.track.duration.seconds % 3600, 60)
        expected = f'{str(dur_min).zfill(2)}:{str(dur_sec).zfill(2)}'
        self.assertEqual(actual, expected)

    def test_explicit_present(self):
        r = self.client.get(self.url)
        actual = self.css_select_get_text(r, 'dl.properties dd#explicit')[0]
        expected = 'Yes' if self.track.is_explicit else 'No'
        self.assertEqual(actual, expected)

    def test_popularity_present(self):
        r = self.client.get(self.url)
        actual = self.css_select_get_text(r, 'dl.properties dd#popularity')[0]
        expected = str(self.track.popularity)
        self.assertEqual(actual, expected)

    def test_artists_present(self):
        r = self.client.get(self.url)
        actual_artist_list = self.css_select_get_text(r, 'ul#artists li.artist a')
        expected_artist_list = [artist.name for artist in self.track.artists.all()]
        expected_artist_list.sort()
        self.assertEqual(actual_artist_list, expected_artist_list)

    def test_link_to_drill_down(self):
        r = self.client.get(self.url)
        actual_urls = self.css_select_get_attributes(
            r, 'ul#artists li.artist a', ['href']
        )
        expected_urls = [
            {'href': reverse('artists:single_artist', kwargs=dict(artist_id=artist.pk))}
            for artist in self.track.artists.all()
        ]
        self.assertCountEqual(actual_urls, expected_urls)
