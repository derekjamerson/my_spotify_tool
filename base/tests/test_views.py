from unittest.mock import patch

from django.test.client import RequestFactory
from django.urls import reverse

from libraries.factories import LibraryFactory
from testing import BaseTestCase
from users.factories import CustomUserFactory


class IndexTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('base:index')
        self.request_factory = RequestFactory()
        self.user = CustomUserFactory()
        self.library = LibraryFactory(user=self.user)

    def test_GET_returns_200(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)

    def test_redirect_page(self):
        self.client.force_login(self.user)
        r = self.client.get(self.url)
        self.assertRedirects(r, reverse('libraries:my_library_stats'))


class SpotifyLoginTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('base:login')

    def test_POST_returns_302(self):
        r = self.client.post(self.url)
        self.assertEqual(r.status_code, 302)


class SpotifyCallbackTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('base:callback')
        self.user = CustomUserFactory()
        self.library = LibraryFactory(user=self.user)

    def test_redirect_login_success(self):
        return_val = {'access_token': 'dummy_access_token'}
        user_dict = {
            'display_name': self.user.username,
            'email': self.user.email,
            'id': self.user.pk,
        }
        with patch('spotify.oauth.OAuth.get_token_json', return_value=return_val):
            with patch('spotify.Spotify.fetch_current_user', return_value=user_dict):
                r = self.client.post(self.url)
        self.assertRedirects(r, reverse('libraries:my_library_stats'))

    def test_redirect_login_fail(self):
        return_val = {'access_token': 'dummy_access_token'}
        with patch('spotify.oauth.OAuth.get_token_json', return_value=return_val):
            with patch('backends.base.AuthBackend.authenticate', return_value=None):
                r = self.client.post(self.url)
        self.assertRedirects(r, reverse('base:index'))


class LogoutViewTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('base:logout')

    def test_redirect_page(self):
        r = self.client.post(self.url)
        self.assertRedirects(r, reverse('base:index'))


class PullDataTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('base:pull_data')

    def test_redirect_page(self):
        session = self.client.session
        session['token_response'] = {'access_token': 'dummy_access_token'}
        session.save()
        with patch('spotify.Spotify.pull_library_data', return_value=None):
            r = self.client.post(self.url)
        self.assertRedirects(r, reverse('base:index'))
