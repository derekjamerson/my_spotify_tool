from libraries.models import Library


class LibraryUtils:
    def add_library_to_db(self, tracks, user):
        library = Library.objects.create(
            tracks=set([track['id'] for track in tracks]),
            user=user,
        )
        artist_pks = set(self.get_all_artist_pks(tracks))
        library.artists.set(artist_pks)

    @staticmethod
    def get_all_artist_pks(tracks):
        for track in tracks:
            for artist in track['artists']:
                yield artist['id']
