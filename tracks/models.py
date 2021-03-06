from datetime import timedelta

from django.db import models


class Track(models.Model):
    objects = models.Manager()
    spotify_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200)
    artists = models.ManyToManyField('artists.Artist', related_name='tracks')
    album = models.ForeignKey(
        'albums.Album', on_delete=models.CASCADE, related_name='tracks'
    )
    duration_ms = models.CharField(max_length=7)
    is_explicit = models.BooleanField(default=False)
    popularity = models.CharField(max_length=3)

    @property
    def duration(self):
        return timedelta(milliseconds=int(self.duration_ms))
