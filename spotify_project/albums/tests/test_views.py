from operator import attrgetter

from albums.factories import AlbumFactory
from artists.factories import ArtistFactory
from django.urls import reverse
from testing import BaseTestCase
from tracks.factories import TrackFactory


class AlbumInfoTestCase(BaseTestCase):
    @property
    def url(self):
        return reverse(
            'albums:album_info',
            kwargs={'album_id': self.album.spotify_id},
        )

    def setUp(self):
        super().setUp()
        self.artists = ArtistFactory.create_batch(3)
        self.album = AlbumFactory(artists=self.artists)
        self.tracks = TrackFactory.create_batch(3, album=self.album)

    def test_GET_returns_200(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)

    def test_properties_present(self):
        r = self.client.get(self.url)
        actual_properties = self.css_select_get_text(r, 'dl.properties dd')
        expected_properties = [
            '',
            '',
            self.album.spotify_id,
            self.album.release_date,
        ]
        self.assertEqual(actual_properties, expected_properties)

    def test_artists_present(self):
        r = self.client.get(self.url)
        actual_artist_list = self.css_select_get_text(r, 'li.artists a')
        expected_artist_list = [artist.name for artist in self.album.artists.all()]
        expected_artist_list.sort(key=attrgetter('name'))
        self.assertEqual(actual_artist_list, expected_artist_list)

    def test_tracks_present(self):
        r = self.client.get(self.url)
        actual_track_list = self.css_select_get_text(r, 'li.tracks a')
        expected_track_list = [track.name for track in self.album.tracks.all()]
        expected_track_list.sort(key=attrgetter('name'))
        self.assertEqual(actual_track_list, expected_track_list)

    def test_link_to_artist_drill_down(self):
        r = self.client.get(self.url)
        actual_urls = self.css_select_get_attributes(r, 'li.artists a', ['href'])
        expected_urls = [
            {'href': reverse('artists:single_artist', kwargs=dict(artist_id=artist.pk))}
            for artist in self.album.artists.all()
        ]
        self.assertCountEqual(actual_urls, expected_urls)

    def test_link_to_track_drill_down(self):
        r = self.client.get(self.url)
        actual_urls = self.css_select_get_attributes(r, 'li.tracks a', ['href'])
        expected_urls = [
            {'href': reverse('tracks:single_track', kwargs=dict(track_id=track.pk))}
            for track in self.album.tracks.all()
        ]
        self.assertCountEqual(actual_urls, expected_urls)
