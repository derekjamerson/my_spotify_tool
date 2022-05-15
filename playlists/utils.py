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

    def create_by_artists(self, user, artists):
        result_playlist = self.name_playlist_by_artist(artists)
        lib_tracks = list(user.library.tracks.all())
        tracks = []
        for artist in artists:
            for track in lib_tracks:
                if artist in track.artists.all():
                    tracks.append(track)
        random.shuffle(tracks)
        result_playlist.tracks = tracks
        return result_playlist

    def name_playlist_by_artist(self, artists):
        string_artists = ''
        if len(artists) == 1:
            title = artists[0].name
            string_artists = title
        elif len(artists) == 2:
            title = f'{artists[0].name} and {artists[1].name}'
            string_artists = f'{artists[0].name} and {artists[1].name}'
        else:
            title = f'{artists[0].name} and Friends'
            for count, artist in enumerate(artists):
                if count == len(artists) - 1:
                    string_artists += f'and {artist.name}'
                else:
                    string_artists += f'{artist.name}, '
        result_playlist = Playlist(
            name=title,
            description=f"{string_artists}. Created with Derek's Spotify Tool",
        )
        return result_playlist
