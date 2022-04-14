from artists.models import Artist


class ArtistUtils:
    def add_artists_to_db(self, tracks):
        unsaved_artists = set(self.get_all_artists(tracks))
        new_artists = self.get_new_artists(unsaved_artists)
        Artist.objects.bulk_create(new_artists)

    @staticmethod
    def get_all_artists(tracks):
        for track in tracks:
            for artist in track['artists']:
                yield Artist(pk=artist['id'], name=artist['name'])
            for artist in track['album']['artists']:
                yield Artist(pk=artist['id'], name=artist['name'])

    @staticmethod
    def get_new_artists(unsaved_artists):
        current_artist_pks = set(Artist.objects.values_list('pk', flat=True))
        for artist in unsaved_artists:
            if artist.pk in current_artist_pks:
                continue
            yield artist
