from testing import BaseTestCase
from users.factories import CustomUserFactory


class AuthBackendTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = CustomUserFactory()
