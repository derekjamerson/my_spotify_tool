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
        self.other_library = LibraryFactory.build(user=self.other_user)
        self.other_library.save()

    def test_GET_returns_200(self):
        r = self.client.get(self.url_other)
        self.assertEqual(r.status_code, 200)
        r = self.client.get(self.url_me)
        self.assertEqual(r.status_code, 200)

    def test_user_name_present(self):
        r = self.client.get(self.url_me)
        actual = self.css_select_get_text(r, 'dl.properties dd#user-name')[0]
        expected = self.user.username
        self.assertEqual(actual, expected)

    def test_last_updated_present(self):
        r = self.client.get(self.url_me)
        actual = self.css_select_get_text(r, 'dl.properties dd#last-updated')[0]
        expected = self.library.last_updated.astimezone(None).strftime(
            '%B %d, %Y %H:%M:%S'
        )
        self.assertEqual(actual, expected)

    def test_track_count_present(self):
        r = self.client.get(self.url_me)
        actual = self.css_select_get_text(r, 'dl.properties dd#track-count')[0]
        expected = str(self.library.tracks.count())
        self.assertEqual(actual, expected)

    def test_artist_count_present(self):
        r = self.client.get(self.url_me)
        actual = self.css_select_get_text(r, 'dl.properties dd#artist-count')[0]
        expected = str(self.library.artists.count())
        self.assertEqual(actual, expected)

    def test_total_duration_present(self):
        r = self.client.get(self.url_me)
        actual = self.css_select_get_text(r, 'dl.properties dd#total-duration')[0]
        hours, remainder = divmod(self.library.total_duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        expected = (
            f'{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}'
        )
        self.assertEqual(actual, expected)

    def test_avg_pop_present(self):
        r = self.client.get(self.url_me)
        actual = self.css_select_get_text(r, 'dl.properties dd#avg-pop')[0]
        expected = str(self.library.avg_pop)
        self.assertEqual(actual, expected)

    def test_top_artists_present(self):
        r = self.client.get(self.url_me)
        actual_artist_list = self.css_select_get_text(
            r, 'dl.properties ul#top-artists li.artist a'
        )
        expected_artist_list = []
        for artist, count in self.library.top_artists.items():
            expected_artist_list.append(f'{artist.name} - {count}')
        self.assertEqual(actual_artist_list, expected_artist_list)

    def test_link_to_drill_down(self):
        r = self.client.get(self.url_me)
        actual_urls = self.css_select_get_attributes(r, 'li.artist a', ['href'])
        expected_urls = [
            {'href': reverse('artists:single_artist', kwargs=dict(artist_id=artist.pk))}
            for artist in self.library.top_artists
        ]
        self.assertCountEqual(actual_urls, expected_urls)

    def test_last_updated_empty(self):
        r = self.client.get(self.url_other)
        actual = self.css_select_get_text(r, 'dl.properties dd#last-updated')[0]
        expected = 'Never'
        self.assertEqual(actual, expected)

    def test_track_count_empty(self):
        r = self.client.get(self.url_other)
        actual = self.css_select_get_text(r, 'dl.properties dd#track-count')[0]
        expected = '0'
        self.assertEqual(actual, expected)

    def test_artist_count_empty(self):
        r = self.client.get(self.url_other)
        actual = self.css_select_get_text(r, 'dl.properties dd#artist-count')[0]
        expected = '0'
        self.assertEqual(actual, expected)

    def test_total_duration_empty(self):
        r = self.client.get(self.url_other)
        actual = self.css_select_get_text(r, 'dl.properties dd#total-duration')[0]
        expected = '00:00:00'
        self.assertEqual(actual, expected)

    def test_avg_pop_empty(self):
        r = self.client.get(self.url_other)
        actual = self.css_select_get_text(r, 'dl.properties dd#avg-pop')[0]
        expected = '0'
        self.assertEqual(actual, expected)

    def test_top_artists_empty(self):
        r = self.client.get(self.url_other)
        actual = self.css_select_get_text(r, 'ul#top-artists')[0]
        expected = 'None'
        self.assertEqual(actual, expected)
