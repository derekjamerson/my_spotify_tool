from albums.factories import AlbumFactory
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

    def test_properties_present(self):
        r = self.client.get(self.url)
        actual_properties = self.css_select_get_text(r, 'dl.properties dd')
        expected_properties = [
            '',
            self.track.album.name,
            self.track.spotify_id,
            str(self.track.duration),
            'Yes' if self.track.is_explicit else 'No',
            str(self.track.popularity),
        ]
        self.assertEqual(actual_properties, expected_properties)

    def test_artists_present(self):
        r = self.client.get(self.url)
        actual_artist_list = self.css_select_get_text(r, 'li.artists a')
        expected_artist_list = [artist.name for artist in self.track.artists.all()]
        self.assertEqual(actual_artist_list, expected_artist_list)

    def test_link_to_drill_down(self):
        r = self.client.get(self.url)
        actual_urls = self.css_select_get_attributes(r, 'li.artists a', ['href'])
        expected_urls = [
            {'href': reverse('artists:single_artist', kwargs=dict(artist_id=artist.pk))}
            for artist in self.track.artists.all()
        ]
        self.assertCountEqual(actual_urls, expected_urls)
