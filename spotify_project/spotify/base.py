from urllib.parse import urlencode

import requests
from albums.models import Album
from artists.models import Artist
from django.contrib.auth import get_user_model
from tracks.models import Track


class Spotify:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}',
        }

    @staticmethod
    def get_response_json(url, headers, limit='50'):
        body = {
            'limit': limit,
        }
        return requests.get(url, headers=headers, params=urlencode(body)).json()

    @property
    def tracks(self):
        library_url = 'https://api.spotify.com/v1/me/tracks'
        response = self.get_response_json(library_url, self.headers)
        while True:
            for track in response['items']:
                yield track['track']
            if response['next'] is None:
                break
            response = self.get_response_json(response['next'], self.headers)

    def fetch_current_user(self):
        profile_url = 'https://api.spotify.com/v1/me'
        spotify_user = self.get_response_json(profile_url, self.headers)
        return spotify_user

    def pull_library_data(self):
        for track in self.tracks:
            self.add_track_to_db(track)
        return

    def add_track_to_db(self, track):
        artists_pks = self.add_array_of_artists(track['artists'])
        album_in_db = self.add_album_to_db(track['album'])
        defaults = {
            'name': track['name'],
            'duration_ms': track['duration_ms'],
            'is_explicit': track['explicit'],
            'popularity': track['popularity'],
            'album': album_in_db,
        }
        track_in_db, created = Track.objects.update_or_create(
            pk=track['id'], defaults=defaults
        )
        track_in_db.artists.add(*artists_pks)
        return created

    def add_array_of_artists(self, artists):
        artists_pks = []
        for artist in artists:
            artists_pks.append(artist['id'])
            self.add_artist_to_db(artist)
        return artists_pks

    @staticmethod
    def add_artist_to_db(artist):
        defaults = {
            'name': artist['name'],
        }
        Artist.objects.update_or_create(pk=artist['id'], defaults=defaults)
        return

    def add_album_to_db(self, album):
        artists_pks = self.add_array_of_artists(album['artists'])
        defaults = {
            'name': album['name'],
        }
        album_in_db, created = Album.objects.update_or_create(
            pk=album['id'], defaults=defaults
        )
        album_in_db.artists.add(*artists_pks)
        return album_in_db
