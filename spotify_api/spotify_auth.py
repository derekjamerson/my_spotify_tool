import os
import requests

from spotify_project.spotify_project.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, REDIRECT_URI


class SpotifyAuth(object):
    authorization_url = 'https://accounts.spotify.com/authorize'
    token_url = 'https://accounts.spotify.com/api/token'
    base_url = 'https://api.spotify.com/v1/'

    def __init__(self, scope_list):
        if scope_list:
            self.scope = scope_list

    @property
    def client_id(self):
        return os.environ.get('SPOTIFY_CLIENT_ID')

    @property
    def client_secret(self):
        return os.environ.get('SPOTIFY_CLIENT_SECRET')

    @property
    def redirect_uri(self):
        return os.environ.get('REDIRECT_URI')

    def get_access_token(self):
        payload = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        token_request = requests.post(url=self.token_url, data=payload, headers=headers)
        token_response = token_request.json()
        return token_response['access_token']
