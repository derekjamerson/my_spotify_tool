import base64
import os
import urllib
from urllib import parse
from urllib.parse import urlencode

import requests


class OAuth:
    auth_endpoint = 'https://accounts.spotify.com/authorize'
    token_uri = 'https://accounts.spotify.com/api/token'
    scope = [
        'users-read-private',
        'users-read-email',
        'users-library-read',
    ]

    def create_auth_url(self):
        payload = {
            'client_id': os.getenv('SPOTIFY_CLIENT_ID'),
            'redirect_uri': os.getenv('REDIRECT_URI'),
            'scope': ' '.join(self.scope),
            'response_type': 'code',
        }
        auth_url = self.auth_endpoint + '?' + urllib.parse.urlencode(payload)
        return auth_url

    def get_token_json(self, auth_response):
        auth_string = (
            os.getenv('SPOTIFY_CLIENT_ID') + ':' + os.getenv('SPOTIFY_CLIENT_SECRET')
        )
        auth_head = base64.b64encode(auth_string.encode('ascii')).decode('ascii')
        headers = {
            'Authorization': 'Basic ' + auth_head,
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        body = {
            'code': auth_response.GET['code'],
            'redirect_uri': os.getenv('REDIRECT_URI'),
            'grant_type': 'authorization_code',
        }
        response_json = requests.post(
            self.token_uri, data=urlencode(body), headers=headers, json=True
        ).json()
        return response_json
