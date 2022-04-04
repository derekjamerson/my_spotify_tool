from unittest import mock

from django.urls import reverse

from testing import BaseTestCase
from tracks.models import Track


class PullDataTestCase(BaseTestCase):
    url = reverse('base:pull_data')

    def get_items(self, num_items=1):
        return [
            {'track': self.get_tracks()} for _ in range(num_items)
        ]

    def get_artists(self, num_artists=1):
        return [
            {'id': '', 'name': ''} for _ in range(num_artists)
        ]

    def get_album(self, num_artists=1):
        return {
            'artists': self.get_artists(num_artists),
            'name': '',
            'id': ''
        }

    def get_tracks(self, num=1):
        return {
            'artists': self.get_artists(),
            'album': self.get_album(),
            'name': '',
            'duration_ms': 1,
            'explicit': True,
            'popularity': 1,
            'id': '',
        }

    def pull_data(self):
        session = self.client.session
        session['token_response'] = {'access_token': 'access_token'}
        session.save()
        return_value = {
            'items': self.get_items(),
            'next': None,
        }
        with mock.patch('spotify.base.Spotify.get_response_json', return_value=return_value):
            r = self.client.get(self.url)
        return r

    def test_GET_returns_200(self):
        r = self.pull_data()
        self.assertEqual(r.status_code, 200)

    def test_tracks_are_created(self):
        with self.assert_num_objects_created({Track: 1}):
            r = self.pull_data()
        self.assertEqual(r.status_code, 200)
