import base64
import urllib.parse
import webbrowser
from urllib.parse import urlencode

import requests

from spotify_project.spotify_project.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, REDIRECT_URI


class SpotifyAuth(object):
    auth_url = 'https://accounts.spotify.com/authorize'
    token_uri = 'https://accounts.spotify.com/api/token'
    access_token = None

    def __init__(self, scope_list):
        if scope_list:
            self.scope = scope_list

    def get_access_token(self):
        authorization_url = self.create_auth_url()
        webbrowser.open(authorization_url)
        auth_resp = input('callback: ').split('?code=')
        token = self.request_token(auth_resp[-1])
        self.access_token = token
        return token

    def create_auth_url(self):
        payload = {
            'client_id': SPOTIFY_CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'scope': self.scope
        }
        return self.auth_url + '?' + urllib.parse.urlencode(payload)

    def request_token(self, auth_code):
        auth_head = base64.b64encode((SPOTIFY_CLIENT_ID + ':' + SPOTIFY_CLIENT_SECRET).encode('ascii')).decode('ascii')
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + auth_head
        }
        body = {
            'code': auth_code,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code'
        }
        self.access_token = requests.post(self.token_uri, data=urlencode(body), headers=headers, json=True).json()
        return self.access_token['access_token']
