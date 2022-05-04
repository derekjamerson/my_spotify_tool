from collections import defaultdict
from datetime import timedelta
from operator import itemgetter

from django.conf import settings
from django.db import models


class Library(models.Model):
    objects = models.Manager()
    tracks = models.ManyToManyField('tracks.Track', related_name='libraries')
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='library',
    )
    artists = models.ManyToManyField('artists.Artist', related_name='libraries')
    last_updated = models.DateTimeField(auto_now_add=True, blank=True)

    @property
    def top_artists(self):
        artist_dict = defaultdict(int)
        for track in self.tracks.all().prefetch_related('artists'):
            for artist in track.artists.all():
                artist_dict[artist] += 1
        list_tuples = list(artist_dict.items())
        list_tuples.sort(key=itemgetter(1), reverse=True)
        result = dict(list_tuples[:10])
        return result

    @property
    def total_duration(self):
        result = 0
        for track in self.tracks.all():
            result += int(track.duration_ms)
        return timedelta(milliseconds=result)

    @property
    def avg_pop(self):
        total_pop = 0
        for track in self.tracks.all():
            total_pop += int(track.popularity)
        try:
            return round(total_pop / self.tracks.count(), 2)
        except ZeroDivisionError:
            return 0
