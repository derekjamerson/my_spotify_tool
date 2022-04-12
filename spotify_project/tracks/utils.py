from tracks.models import Track


class TrackUtils:
    def add_tracks_to_db(self, tracks):
        unsaved_tracks = set(self.get_all_tracks(tracks))
        new_tracks = self.get_new_tracks(unsaved_tracks)
        Track.objects.bulk_create(new_tracks)

    @staticmethod
    def get_all_tracks(tracks):
        for track in tracks:
            yield Track(
                pk=track['id'],
                name=track['name'],
                album=track['album']['id'],
                duration=track['duration_ms'],
                is_explicit=track['is_explicit'],
                popularity=track['popularity'],
            )

    @staticmethod
    def get_new_tracks(unsaved_tracks):
        current_track_pks = set(Track.objects.values_list('pk', flat=True))
        for track in unsaved_tracks:
            if track.pk in current_track_pks:
                continue
            yield track

    def add_track_artist_m2m(self, tracks):
        unsaved_throughs = set(self.get_all_track_artist_throughs(tracks))
        new_throughs = self.get_new_track_artist_throughs(unsaved_throughs)
        Track.artists.through.objects.bulk_create(new_throughs)

    @staticmethod
    def get_all_track_artist_throughs(tracks):
        for track in tracks:
            for artist in track['track']['artists']:
                yield track['track']['id'], artist['id']

    @staticmethod
    def get_new_track_artist_throughs(unsaved_throughs):
        current_throughs = set(
            [(x.track, x.artist) for x in Track.artists.through.objects.all()]
        )
        for new_through in unsaved_throughs:
            if new_through in current_throughs:
                continue
            yield Track.artists.through(track=new_through[0], artist=new_through[1])
