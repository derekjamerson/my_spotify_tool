from django.db import models


class Artist(models.Model):
    objects = models.Manager()
    spotify_id = models.CharField(max_length=22, primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
