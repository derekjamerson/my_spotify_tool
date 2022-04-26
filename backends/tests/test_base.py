from unittest.mock import patch

from backends.base import AuthBackend
from testing import BaseTestCase
from users.factories import CustomUserFactory


class AuthBackendTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = CustomUserFactory.build()

    def test_authenticate(self):
        user_dict = {
            'display_name': self.user.username,
            'email': self.user.email,
            'id': self.user.pk,
        }
        auth_back = AuthBackend()
        with patch('spotify.Spotify.fetch_current_user', return_value=user_dict):
            self.assertEqual(auth_back.authenticate(request=' '), self.user)
            r = auth_back.authenticate(request=' ')
        self.assertEqual(r.pk, self.user.pk)
        self.assertEqual(r.email, self.user.email)
        self.assertEqual(r.username, self.user.username)

    def test_get_user(self):
        auth_back = AuthBackend()
        self.assertIsNone(auth_back.get_user(self.user.pk))
        self.user.save()
        r = auth_back.get_user(self.user.pk)
        self.assertEqual(r.pk, self.user.pk)
        self.assertEqual(r.email, self.user.email)
        self.assertEqual(r.username, self.user.username)
