from urllib.parse import urlencode

import requests

from tracks.models import Track


class Spotify:
    def __init__(self, token):
        self.token = token

    @staticmethod
    def get_response_json(url, headers, limit='50'):
        body = {
            'limit': limit,
        }
        return requests.get(url, headers=headers, params=urlencode(body)).json()

    @property
    def tracks(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}',
        }
        library_url = 'https://api.spotify.com/v1/me/tracks'
        response = self.get_response_json(library_url, headers)
        while True:
            for track in response['items']:
                yield track['track']
            if response['next'] is None:
                break
            response = self.get_response_json(response['next'], headers)

    def pull_library_data(self):
        counter = 0
        for track in self.tracks:
            Track.objects.create(pk=track['id'], name=track['name'])
            counter += 1
        return counter
