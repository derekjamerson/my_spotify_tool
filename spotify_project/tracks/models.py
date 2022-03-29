from django.db import models

# Create your models here.


class Track(models.Model):
    name = models.CharField(max_length=200)
    spotify_id = models.CharField(max_length=22, primary_key=True)
# 1-many album. models.manytomany for artists.
