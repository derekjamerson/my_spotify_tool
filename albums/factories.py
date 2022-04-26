import uuid

import factory
from faker import Faker

from albums.models import Album


# noinspection PyMethodParameters
class AlbumFactory(factory.django.DjangoModelFactory):
    @factory.Sequence
    def name(n):
        return str(uuid.uuid4())

    @factory.Sequence
    def spotify_id(n):
        return str(uuid.uuid4())

    @factory.post_generation
    def artists(self, create, artists):
        if not create or not artists:
            return

        self.artists.add(*artists)

    @factory.Sequence
    def release_date(n):
        return Faker().date()

    class Meta:
        model = Album
