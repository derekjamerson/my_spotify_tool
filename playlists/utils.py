import random

from playlists.models import Playlist


class PlaylistUtils:
    def create_random(self, user):
        result_playlist = Playlist(
            name="True Random", description="Created with Derek's Spotify Tool"
        )
        tracks = user.library.tracks.order_by('?')
        result_playlist.tracks = tracks
        return result_playlist

    def create_by_artists(self, *, user, artists, name):
        description = "Created by Derek's App"
        result_playlist = Playlist(name=name, description=description)
        lib_tracks = list(user.library.tracks.filter(artists__in=artists))
        tracks = []
        for track in lib_tracks:
            tracks.append(track)
        random.shuffle(tracks)
        result_playlist.tracks = tracks
        return result_playlist
