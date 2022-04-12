from urllib.parse import urlencode

import requests
from albums.models import Album
from artists.models import Artist
from libraries.models import Library
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

    def pull_library_data(self, user):
        tracks_dicts = list(self.tracks)
        unsaved_artists = set(self.get_all_artists(tracks_dicts))
        self.add_artists_to_db(unsaved_artists)
        unsaved_albums = set(self.get_all_albums(tracks_dicts))
        self.add_albums_to_db(unsaved_albums)
        unsaved_tracks = set(self.get_all_tracks(tracks_dicts))
        self.add_tracks_to_db(unsaved_tracks)
        unsaved_a_a_thrus = set(self.get_all_a_a_thru(tracks_dicts))
        self.add_a_a_thru_to_db(unsaved_a_a_thrus)
        unsaved_t_a_thrus = set(self.get_all_t_a_thru(tracks_dicts))
        self.add_t_a_thru_to_db(unsaved_t_a_thrus)
        return

    def get_all_artists(self, tracks):
        for track in tracks:
            for artist in track['artists']:
                yield Artist(pk=artist['id'], name=artist['name'])
            for artist in track['album']['artists']:
                yield Artist(pk=artist['id'], name=artist['name'])

    def add_artists_to_db(self, artists_dicts):
        current_artist_pks = set(Artist.objects.values_list('pk', flat=True))
        new_artists = self.get_new_artists(current_artist_pks, artists_dicts)
        Artist.objects.bulk_create(new_artists)

    def get_new_artists(self, old_pks, unsaved_artists):
        for artist in unsaved_artists:
            if artist.pk in old_pks:
                continue
            yield artist

    def get_all_albums(self, tracks):
        for track in tracks:
            yield Album(pk=track['album']['id'], name=track['album']['name'])

    def add_albums_to_db(self, unsaved_albums):
        current_album_pks = set(Album.objects.values_list('pk', flat=True))
        new_albums = self.get_new_albums(current_album_pks, unsaved_albums)
        Album.objects.bulk_create(new_albums)

    def get_new_albums(self, current_album_pks, unsaved_albums):
        for album in unsaved_albums:
            if album.pk in current_album_pks:
                continue
            yield album

    def get_all_tracks(self, tracks):
        for track in tracks:
            yield Track(
                pk=track['id'],
                name=track['name'],
                album=track['album']['id'],
                duration=track['duration_ms'],
                is_explicit=track['is_explicit'],
                popularity=track['popularity'],
            )

    def add_tracks_to_db(self, unsaved_tracks):
        current_track_pks = set(Track.objects.values_list('pk', flat=True))
        new_tracks = self.get_new_tracks(current_track_pks, unsaved_tracks)
        Track.objects.bulk_create(new_tracks)

    def get_new_tracks(self, current_track_pks, unsaved_tracks):
        for track in unsaved_tracks:
            if track.pk in current_track_pks:
                continue
            yield track

    def get_all_a_a_thru(self, tracks):
        for track in tracks:
            for artist in track['album']['artists']:
                yield track['album']['id'], artist['id']

    def add_a_a_thru_to_db(self, unsaved_a_a_thrus):
        current_a_a_thrus = set(
            [(x.album, x.artist) for x in Album.artists.through.objects.all()]
        )
        new_a_a_thrus = self.get_new_a_a_thrus(current_a_a_thrus, unsaved_a_a_thrus)
        Album.artists.through.objects.bulk_create(new_a_a_thrus)

    def get_new_a_a_thrus(self, current_a_a_thrus, unsaved_a_a_thrus):
        for new_through in unsaved_a_a_thrus:
            if new_through in current_a_a_thrus:
                continue
            yield Album.artists.through(album=new_through[0], artist=new_through[1])

    def get_all_t_a_thru(self, tracks):
        for track in tracks:
            for artist in track['track']['artists']:
                yield track['track']['id'], artist['id']

    def add_t_a_thru_to_db(self, unsaved_t_a_thrus):
        current_t_a_thrus = set(
            [(x.track, x.artist) for x in Track.artists.through.objects.all()]
        )
        new_t_a_thrus = self.get_new_t_a_thrus(current_t_a_thrus, unsaved_t_a_thrus)
        Track.artists.through.objects.bulk_create(new_t_a_thrus)

    def get_new_t_a_thrus(self, current_t_a_thrus, unsaved_t_a_thrus):
        for new_through in unsaved_t_a_thrus:
            if new_through in current_t_a_thrus:
                continue
            yield Track.artists.through(track=new_through[0], artist=new_through[1])
