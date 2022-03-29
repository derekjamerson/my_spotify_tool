from django.db import models

from albums.models import Album
from artists.models import Artist


class Track(models.Model):
    objects = models.Manager()
    spotify_id = models.CharField(max_length=22, primary_key=True)
    name = models.CharField(max_length=200)
    artists = models.ManyToManyField(Artist, related_name='tracks')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks')
    duration_ms = models.CharField(max_length=6)
    is_explicit = models.BooleanField(default=False)
    popularity = models.CharField(max_length=3)

    def __str__(self):
        return self.name
