from urllib.parse import urlencode

import requests

from artists.models import Artist
from tracks.models import Track


class Spotify:
    def __init__(self, token):
        self.token = token
        self.created_rows = {
            'tracks': 0,
            'artists': 0,
            'albums': 0,
        }

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
        for track in self.tracks:
            created = self.add_track_to_db(track)
            if created:
                self.created_rows['tracks'] += 1
        return self.created_rows

    def add_track_to_db(self, track):
        artists_pks = []
        for artist in track['artists']:
            artists_pks.append(artist['id'])
            created = self.add_artist_to_db(artist)
            if created:
                self.created_rows['artists'] += 1
        defaults = {
            'name': track['name'],
        }
        track_in_db, created = Track.objects.update_or_create(pk=track['id'], defaults=defaults)
        track_in_db.artists.add(*artists_pks)
        return created

    @staticmethod
    def add_artist_to_db(artist):
        defaults = {
            'name': artist['name'],
        }
        artist_in_db, created = Artist.objects.update_or_create(pk=artist['id'], defaults=defaults)
        return created
