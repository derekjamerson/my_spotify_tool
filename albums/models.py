from django.db import models


class Album(models.Model):
    objects = models.Manager()
    spotify_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200)
    artists = models.ManyToManyField('artists.Artist', related_name='albums')
    release_date = models.CharField(max_length=10)

    def __str__(self):
        return self.name
