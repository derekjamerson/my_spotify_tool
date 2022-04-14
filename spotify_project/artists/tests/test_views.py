from operator import attrgetter

from artists.factories import ArtistFactory
from django.urls import reverse
from libraries.factories import LibraryFactory
from testing import BaseTestCase
from tracks.factories import TrackFactory
from users.factories import CustomUserFactory


class AllArtistsTestCase(BaseTestCase):
    url = reverse('artists:my_artists')

    def setUp(self):
        super().setUp()
        self.user = CustomUserFactory()
        self.artist = ArtistFactory()
        self.library = LibraryFactory(user=self.user, artists=[self.artist])
        self.client.force_login(self.user)
        # not included
        ArtistFactory()

    def test_GET_returns_200(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)

    def test_artist_name_sorted(self):
        r = self.client.get(self.url)
        actual_names = self.css_select_get_text(r, 'td.artist-name')
        expected_names = list(
            self.library.artists.values_list('name', flat=True).order_by('name')
        )
        self.assertEqual(actual_names, expected_names)

    def test_link_to_drill_down(self):
        r = self.client.get(self.url)
        actual_urls = self.css_select_get_attributes(r, 'td.artist-name a', ['href'])
        expected_urls = [
            {'href': reverse('artists:single_artist', kwargs=dict(artist_id=artist.pk))}
            for artist in self.library.artists.all()
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
        self.user = CustomUserFactory()
        self.artist = ArtistFactory()
        self.tracks = TrackFactory.create_batch(3, artists=[self.artist])
        self.library = LibraryFactory(
            user=self.user, tracks=self.tracks, artists=[self.artist]
        )
        self.client.force_login(self.user)
        # not included
        ArtistFactory()
        TrackFactory()

    def test_GET_returns_200(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)

    def test_track_names_sorted(self):
        r = self.client.get(self.url)
        actual_names = self.css_select_get_text(r, 'td.track-name')
        self.tracks.sort(key=attrgetter('name'))
        expected_names = [track.name for track in self.tracks]
        self.assertEqual(actual_names, expected_names)

    def test_link_to_drill_down(self):
        r = self.client.get(self.url)
        actual_urls = self.css_select_get_attributes(r, 'td.track-name a', ['href'])
        expected_urls = [
            {'href': reverse('tracks:track_info', kwargs=dict(track_id=track.pk))}
            for track in self.tracks
        ]
        self.assertCountEqual(actual_urls, expected_urls)
