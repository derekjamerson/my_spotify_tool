from django.db import models


class Track(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=200)
    spotify_id = models.CharField(max_length=22, primary_key=True)
# 1-many album. models.manytomany for artists.
