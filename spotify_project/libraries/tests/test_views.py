from django.urls import reverse
from libraries.factories import LibraryFactory
from testing import BaseTestCase
from users.factories import CustomUserFactory


class LibraryStatsTestCase(BaseTestCase):
    @property
    def url_other(self):
        return reverse(
            'libraries:library_stats',
            kwargs={'user_id': self.other_user.spotify_id},
        )

    url_me = reverse('libraries:my_library_stats')

    def setUp(self):
        super().setUp()
        self.user = CustomUserFactory()
        self.library = LibraryFactory(user=self.user)
        self.client.force_login(self.user)
        self.other_user = CustomUserFactory()
        self.other_library = LibraryFactory(user=self.other_user)
        self.other_library.tracks.clear()
        self.other_library.artists.clear()

    def test_GET_returns_200(self):
        r = self.client.get(self.url_other)
        self.assertEqual(r.status_code, 200)
        r = self.client.get(self.url_me)
        self.assertEqual(r.status_code, 200)

    def test_properties_present(self):
        r = self.client.get(self.url_me)
        actual_properties = self.css_select_get_text(r, 'dd.property')
        expected_properties = [
            self.user.username,
            self.library.last_updated_iso,
            str(self.library.count_tracks),
            str(self.library.count_artists),
            self.library.total_duration,
            str(self.library.avg_pop),
        ]
        self.assertEqual(actual_properties, expected_properties)

    def test_artists_present(self):
        r = self.client.get(self.url_me)
        actual_artist_list = self.css_select_get_text(r, 'li.artists a')
        expected_artist_list = [artist.name for artist in self.library.top_artists]
        self.assertEqual(actual_artist_list, expected_artist_list)

    def test_link_to_drill_down(self):
        r = self.client.get(self.url_me)
        actual_urls = self.css_select_get_attributes(r, 'li.artist a', ['href'])
        expected_urls = [
            {'href': reverse('artists:single_artist', kwargs=dict(artist_id=artist.pk))}
            for artist in self.library.top_artists
        ]
        self.assertCountEqual(actual_urls, expected_urls)

    def test_no_tracks(self):
        r = self.client.get(self.url_other)
        actual_properties = self.css_select_get_text(r, 'dd.property')
        expected_properties = [
            self.other_user.username,
            self.other_library.last_updated_iso,
            '0',
            '0',
            '0',
            '0',
        ]
        self.assertEqual(actual_properties, expected_properties)
