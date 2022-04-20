from unittest.mock import patch

from testing import BaseTestCase
from users.factories import CustomUserFactory
from users.models import CustomUser


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
        with patch('spotify.Spotify.fetch_current_user', return_value=user_dict):
            self.assertTrue(self.user.is_authenticated)
