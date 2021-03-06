from libraries.models import Library


class LibraryUtils:
    def add_library_to_db(self, tracks_dict, user):
        user.library.delete()
        library = Library.objects.create(
            user=user,
        )
        tracks = list(tracks_dict)
        track_pks = set([track['id'] for track in tracks])
        library.tracks.set(track_pks)
        artist_pks = self.get_all_artist_pks(tracks)
        library.artists.set(artist_pks)

    @staticmethod
    def get_all_artist_pks(tracks):
        for track in tracks:
            for artist in track['artists']:
                yield artist['id']
