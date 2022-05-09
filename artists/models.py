from django.db import models


class Artist(models.Model):
    objects = models.Manager()
    spotify_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200)
