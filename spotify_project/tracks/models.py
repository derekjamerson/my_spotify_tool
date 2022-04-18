from django.db import models


class Track(models.Model):
    objects = models.Manager()
    spotify_id = models.CharField(max_length=22, primary_key=True)
    name = models.CharField(max_length=200)
    artists = models.ManyToManyField('artists.Artist', related_name='tracks')
    album = models.ForeignKey(
        'albums.Album', on_delete=models.CASCADE, related_name='tracks'
    )
    duration_ms = models.CharField(max_length=7)
    is_explicit = models.BooleanField(default=False)
    popularity = models.CharField(max_length=3)

    @property
    def duration_string(self):
        # noinspection PyTypeChecker
        seconds, milliseconds = divmod(int(self.duration_ms), 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return f'{hours:02d}:{minutes:02d}:{seconds:02d}'
        if minutes:
            return f'{minutes:02d}:{seconds:02d}'
        return str(seconds)
