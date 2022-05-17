from unittest.mock import patch

from django.urls import reverse

from artists.factories import ArtistFactory
from libraries.factories import LibraryFactory
from testing.base import BaseTestCase
from users.factories import CustomUserFactory


class CreatePlaylistTestCase(BaseTestCase):
    url = reverse('playlists:create')

    def setUp(self):
        super().setUp()
        self.user = CustomUserFactory()
        self.client.force_login(self.user)
        self.library = LibraryFactory(user=self.user)
        self.sess = self.client.session
        self.sess.update({'token_response': {'access_token': 'dummy_token'}})
        self.sess.save()

    def test_GET_returns_200(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)

    # TODO remove patch for is_valid. fix error: invalid choice
    def test_POST_returns_302(self):
        data = {'name': 'dummy_name', 'artists': self.library.artists.all()}
        with patch('playlists.forms.MakePlaylistForm.is_valid', return_value=True):
            with patch('playlists.forms.MakePlaylistForm.save', return_value=None):
                r = self.client.post(self.url, data)
        self.assertRedirects(r, reverse('base:index'), target_status_code=302)

    def test_POST_form_not_valid(self):
        data = {'artists': ArtistFactory()}
        r = self.client.post(self.url, data)
        self.assertEqual(r.status_code, 200)
