from operator import attrgetter

from artists.factories import ArtistFactory
from artists.models import Artist
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
        expected_properties = list(
            self.objects.values_list('name', flat=True).order_by('name')
        )
        self.assertEqual(actual_properties, expected_properties)

    def test_link_to_drill_down(self):
        r = self.client.get(self.url)
        actual_urls = self.css_select_get_attributes(r, 'td.artist-name a', ['href'])
        expected_urls = [
            {'href': reverse('artists:single_artist', kwargs=dict(artist_id=artist.pk))}
            for artist in Artist.objects.all()
        ]
        self.assertCountEqual(actual_urls, expected_urls)


class SingleArtistTestCase(BaseTestCase):
    @property
    def url(self):
        return reverse(
            'artists:single_artist',
            kwargs={'artist_id': self.artist.spotify_id},
        )

    def setUp(self):
        super().setUp()
        self.artist = ArtistFactory()
        self.tracks = TrackFactory.create_batch(3)
        for track in self.tracks:
            track.artists.add(self.artist)
        # not included
        TrackFactory()

    def test_GET_returns_200(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)

    def test_track_names_present(self):
        r = self.client.get(self.url)
        actual_names = self.css_select_get_text(r, 'td.track-name')
        self.tracks.sort(key=attrgetter('name'))
        expected_names = [track.name for track in self.tracks]
        self.assertEqual(actual_names, expected_names)
