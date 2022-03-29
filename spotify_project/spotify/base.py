import requests


class Spotify:
    def __init__(self, token):
        self.token = token

    @staticmethod
    def get_response_json(url, headers):
        return requests.get(url, headers=headers, data={'limit': '50'}).json()

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
