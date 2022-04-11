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
        artists_dicts = set(self.get_all_artists(tracks_dicts))
        self.add_artists_to_db(artists_dicts)
        # get albums in db
        # check against new
        # create album objects
        # get tracks in db
        # check against new
        # create track objects
        # to create m2m
        #  pull through table
        #    album-artist
        #    track-artist
        #  create through table objects
        #    Album.artist.through(album_id=asdjifnalif, artist_id=jasndf;ajndf)
        # bulk_create()
        return

    def get_all_artists(self, tracks):
        for track in tracks:
            for artist in track['artists']:
                yield Artist(pk=artist['id'], name=artist['name'])
            for artist in track['album']['artists']:
                yield Artist(pk=artist['id'], name=artist['name'])

    def add_artists_to_db(self, artists_dicts):
        old_artists_pks = set(Artist.objects.values_list('pk', flat=True))
        new_artists = self.get_new_artists(old_artists_pks, artists_dicts)
        Artist.objects.bulk_create(new_artists)

    def get_new_artists(self, old_pks, artists_dicts):
        for artist in artists_dicts:
            if artist.pk in old_pks:
                continue
            yield artist

    def add_tracks_to_library(self, user, tracks):
        Library.objects.filter(user=user).delete()
        library = Library.objects.create(user=user)
        library.tracks.add(*tracks)
        self.add_artists_to_library(library, tracks)
        return

    @staticmethod
    def add_artists_to_library(library, tracks):
        hold_artists = set()
        for track in tracks:
            hold_artists.update([artist for artist in track.artists.all()])
        library.artists.add(*hold_artists)
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
        return track_in_db

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
