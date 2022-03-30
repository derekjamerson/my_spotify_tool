from django.db import models

from artists.models import Artist


class Album(models.Model):
    objects = models.Manager()
    spotify_id = models.CharField(max_length=22, primary_key=True)
    name = models.CharField(max_length=200)
    artists = models.ManyToManyField('artists.Artist', related_name='albums')

    def __str__(self):
        return self.name
