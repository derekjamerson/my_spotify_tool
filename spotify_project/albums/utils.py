from albums.models import Album


class AlbumUtils:
    def add_albums_to_db(self, tracks):
        unsaved_albums = set(self.get_all_albums(tracks))
        new_albums = self.get_new_albums(unsaved_albums)
        Album.objects.bulk_create(new_albums)

    @staticmethod
    def get_all_albums(tracks):
        for track in tracks:
            yield Album(pk=track['album']['id'], name=track['album']['name'])

    @staticmethod
    def get_new_albums(unsaved_albums):
        current_album_pks = set(Album.objects.values_list('pk', flat=True))
        for album in unsaved_albums:
            if album.pk in current_album_pks:
                continue
            yield album

    def add_album_artist_m2m(self, tracks):
        unsaved_throughs = set(self.get_all_album_artist_throughs(tracks))
        new_throughs = self.get_new_album_artist_throughs(unsaved_throughs)
        Album.artists.through.objects.bulk_create(new_throughs)

    @staticmethod
    def get_all_album_artist_throughs(tracks):
        for track in tracks:
            for artist in track['album']['artists']:
                yield track['album']['id'], artist['id']

    @staticmethod
    def get_new_album_artist_throughs(unsaved_throughs):
        current_throughs = set(
            [(x.album_id, x.artist_id) for x in Album.artists.through.objects.all()]
        )
        for album_id, artist_id in unsaved_throughs:
            if (album_id, artist_id) in current_throughs:
                continue
            yield Album.artists.through(album_id=album_id, artist_id=artist_id)
