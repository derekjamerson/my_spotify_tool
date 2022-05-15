import uuid

from playlists.models import Playlist
from tracks.factories import TrackFactory


class PlaylistFactory:
    def __init__(self, *tracks):
        self.playlist = Playlist(
            spotify_id=str(uuid.uuid4()),
            name=str(uuid.uuid4()),
            tracks=tracks or TrackFactory.create_batch(2),
            description=str(uuid.uuid4()),
        )
