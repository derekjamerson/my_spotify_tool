from operator import attrgetter

from artists.factories import ArtistFactory
from artists.models import Artist
from artists.views import all_artists, single_artist
from django.test import Client, RequestFactory
from django.urls import reverse
from libraries.factories import LibraryFactory
from testing import BaseTestCase
from tracks.factories import TrackFactory
from users.factories import CustomUserFactory


class AllArtistsTestCase(BaseTestCase):
    url = reverse('artists:all_artists')

    def setUp(self):
        super().setUp()
        request_factory = RequestFactory()
        self.request = request_factory.get(self.url)
        user = CustomUserFactory()
        self.request.user = user
        self.library = LibraryFactory(user=user)
        self.artist = ArtistFactory()
        self.tracks = TrackFactory.create_batch(3)
        for track in self.tracks:
            track.artists.add(self.artist)
        self.library.tracks.add(*self.tracks)
        hold_artists = set()
        for track in self.tracks:
            hold_artists.update([artist for artist in track.artists.all()])
        self.library.artists.add(*hold_artists)
        # not included
        dummy_artist = ArtistFactory()
        dummy_track = TrackFactory()
        dummy_track.artists.add(dummy_artist)

    def test_GET_returns_200(self):
        r = all_artists(self.request)
        self.assertEqual(r.status_code, 200)

    def test_artist_name_sorted(self):
        r = all_artists(self.request)
        actual_names = self.css_select_get_text(r, 'td.artist-name')
        expected_names = list(
            self.request.user.library.artists.values_list('name', flat=True).order_by(
                'name'
            )
        )
        self.assertEqual(actual_names, expected_names)

    def test_link_to_drill_down(self):
        r = all_artists(self.request)
        actual_urls = self.css_select_get_attributes(r, 'td.artist-name a', ['href'])
        expected_urls = [
            {'href': reverse('artists:single_artist', kwargs=dict(artist_id=artist.pk))}
            for artist in self.request.user.library.artists.all()
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
        request_factory = RequestFactory()
        self.artist = ArtistFactory()
        self.request = request_factory.get(self.url)
        user = CustomUserFactory()
        self.request.user = user
        self.library = LibraryFactory(user=user)
        self.tracks = TrackFactory.create_batch(3)
        for track in self.tracks:
            track.artists.add(self.artist)
        self.library.tracks.add(*self.tracks)
        hold_artists = set()
        for track in self.tracks:
            hold_artists.update([artist for artist in track.artists.all()])
        self.library.artists.add(*hold_artists)
        # not included
        dummy_artist = ArtistFactory()
        dummy_track = TrackFactory()
        dummy_track.artists.add(dummy_artist)

    def test_GET_returns_200(self):
        r = single_artist(self.request, self.artist.pk)
        self.assertEqual(r.status_code, 200)

    def test_track_names_sorted(self):
        r = single_artist(self.request, self.artist.pk)
        actual_names = self.css_select_get_text(r, 'td.track-name')
        self.tracks.sort(key=attrgetter('name'))
        expected_names = [track.name for track in self.tracks]
        self.assertEqual(actual_names, expected_names)

    def test_link_to_drill_down(self):
        r = single_artist(self.request, self.artist.pk)
        actual_urls = self.css_select_get_attributes(r, 'td.track-name a', ['href'])
        expected_urls = [
            {'href': reverse('tracks:track_info', kwargs=dict(track_id=track.pk))}
            for track in self.artist.tracks.all()
        ]
        self.assertCountEqual(actual_urls, expected_urls)
