from playlists.models import Playlist


class PlaylistUtils:
    def create_random(self, user):
        result_playlist = Playlist(
            name="True Random", description="Created with Derek's Spotify Tool"
        )
        library = user.library
        tracks = library.tracks.order_by('?')[:100]
        result_playlist.tracks = tracks
        return result_playlist
