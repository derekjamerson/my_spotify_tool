from urllib.parse import urlencode

import requests
from albums.utils import AlbumUtils
from artists.utils import ArtistUtils
from libraries.utils import LibraryUtils
from tracks.utils import TrackUtils


# TODO test this. come up with data.
class Spotify:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}',
        }
        self.artist_utils = ArtistUtils()
        self.album_utils = AlbumUtils()
        self.track_utils = TrackUtils()
        self.library_utils = LibraryUtils()

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

    def pull_library_data(self, user):
        track_dicts = list(self.tracks)
        self.artist_utils.add_artists_to_db(track_dicts)
        self.album_utils.add_albums_to_db(track_dicts)
        self.track_utils.add_tracks_to_db(track_dicts)
        self.album_utils.add_album_artist_m2m(track_dicts)
        self.track_utils.add_track_artist_m2m(track_dicts)
        self.library_utils.add_library_to_db(track_dicts, user)
        return
