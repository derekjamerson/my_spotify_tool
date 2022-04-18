from django.urls import reverse
from libraries.factories import LibraryFactory
from testing import BaseTestCase
from users.factories import CustomUserFactory


class UserInfoTestCase(BaseTestCase):
    @property
    def url_user(self):
        return reverse(
            'users:user_info',
            kwargs={'user_id': self.user.spotify_id},
        )

    url_me = reverse('users:my_info')

    def setUp(self):
        super().setUp()
        self.user = CustomUserFactory()
        self.library = LibraryFactory(user=self.user)
        self.client.force_login(self.user)

    def test_GET_returns_200(self):
        r = self.client.get(self.url_user)
        self.assertEqual(r.status_code, 200)
        r = self.client.get(self.url_me)
        self.assertEqual(r.status_code, 200)

    def test_properties_present(self):
        r = self.client.get(self.url_me)
        actual_properties = self.css_select_get_text(r, 'dd.property')
        expected_properties = [
            self.user.username,
            self.user.email,
            self.user.spotify_id,
            str(self.user.library.count_tracks),
        ]
        self.assertEqual(actual_properties, expected_properties)

    def test_link_to_drill_down(self):
        r = self.client.get(self.url_me)
        actual_urls = self.css_select_get_attributes(r, 'a.track-count', ['href'])
        expected_urls = [
            {
                'href': reverse(
                    'libraries:library_stats', kwargs={'user_id': self.user.pk}
                )
            }
        ]
        self.assertCountEqual(actual_urls, expected_urls)