class Playlist:
    def __init__(self, *, spotify_id=None, name, tracks=None, description):
        self.spotify_id = spotify_id
        self.name = name
        self.tracks = tracks
        self.description = description

    @property
    def track_uris(self):
        for track in self.tracks:
            yield track.uri
