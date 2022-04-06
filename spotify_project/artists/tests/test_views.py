from operator import attrgetter

from artists.factories import ArtistFactory
from artists.models import Artist
from django.urls import reverse
from testing import BaseTestCase
from tracks.factories import TrackFactory


class AllArtistsTestCase(BaseTestCase):
    url = reverse('artists:all_artists')

    def setUp(self):
        super().setUp()
        ArtistFactory.create_batch(3)

    def test_GET_returns_200(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)

    def test_artist_name_sorted(self):
        r = self.client.get(self.url)
        actual_names = self.css_select_get_text(r, 'td.artist-name')
        expected_names = list(
            Artist.objects.values_list('name', flat=True).order_by('name')
        )
        self.assertEqual(actual_names, expected_names)

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
