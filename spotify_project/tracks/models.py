from django.db import models


class Track(models.Model):
    objects = models.Manager()
    spotify_id = models.CharField(max_length=22, primary_key=True)
    name = models.CharField(max_length=200)
    artists = models.ManyToManyField('artists.Artist', related_name='tracks')
    album = models.ForeignKey(
        'albums.Album', on_delete=models.CASCADE, related_name='tracks'
    )
    duration_ms = models.CharField(max_length=6)
    is_explicit = models.BooleanField(default=False)
    popularity = models.CharField(max_length=3)

    @property
    def duration(self):
        seconds = (int(self.duration_ms) / 1000) % 60
        minutes = (int(self.duration_ms) / (1000 * 60)) % 60
        return f'{int(minutes)}:{round(seconds)}'

    @duration.setter
    def duration(self, value):
        self.duration_ms = value

    def __str__(self):
        return self.name
