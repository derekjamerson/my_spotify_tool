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
        self.session = requests.Session()

    def get_response_json(self, url, headers, limit='50'):
        body = {
            'limit': limit,
        }
        return self.session.get(url, headers=headers, params=urlencode(body)).json()

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

    def create_playlist(self, user, playlist):
        url = f'https://api.spotify.com/v1/users/{user.pk}/playlists'
        data = {
            'name': playlist.name,
            'description': playlist.description,
            'public': 'true',
        }
        response = self.session.post(url=url, headers=self.headers, data=data).json()
        playlist.spotify_id = response['id']
        playlist.name = response['name']
        if playlist.tracks:
            self.add_tracks_to_playlist(user, playlist)
        return

    def add_tracks_to_playlist(self, user, playlist):
        url = f'https://api.spotify.com/v1/playlists/{playlist.spotify_id}/tracks'
        data = {'uris': []}
        for track in playlist.track_uris:
            data['uris'].append(track)
            if len(data['uris']) == 100:
                self.session.post(url, headers=self.headers, data=data)
                data['uris'] = []
        if data['uris']:
            self.session.post(url, headers=self.headers, data=data)
        return
