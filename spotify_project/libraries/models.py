from collections import defaultdict
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
    def last_updated_iso(self):
        # noinspection PyUnresolvedReferences
        updated_tz = self.last_updated.astimezone(None)
        time_string = updated_tz.isoformat(sep=' ', timespec='seconds')
        return time_string[:19]

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
        seconds, milliseconds = divmod(result, 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        if days:
            return f'{days:03d}:{hours:02d}:{minutes:02d}:{seconds:02d}'
        if hours:
            return f'{hours:02d}:{minutes:02d}:{seconds:02d}'
        if minutes:
            return f'{minutes:02d}:{seconds:02d}'
        return str(seconds)
