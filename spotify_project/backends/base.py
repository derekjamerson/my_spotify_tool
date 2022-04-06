from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

from spotify import Spotify


class AuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, access_token=None):
        spotify = Spotify(access_token)
        spot_user = spotify.fetch_current_user()
        defaults = {
            'username': spot_user['display_name'] or spot_user['email'],
            'email': spot_user['email'],
        }
        user, created = get_user_model().objects.update_or_create(pk=spot_user['id'], defaults=defaults)
        return user
