from django.db import models


class Library(models.Model):
    objects = models.Manager()
    tracks = models.ManyToManyField('tracks.Track', related_name='libraries')
    user = models.OneToOneField(
        'users.CustomUser',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='library',
    )
    artists = models.ManyToManyField('artists.Artist', related_name='libraries')
