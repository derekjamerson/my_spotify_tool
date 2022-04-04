import random
import uuid

import factory

from albums.models import Album
from artists.factories import ArtistFactory
from tracks.models import Track


class AlbumFactory(factory.django.DjangoModelFactory):
    @factory.Sequence
    def name(n):
        return str(uuid.uuid4())

    @factory.Sequence
    def spotify_id(n):
        return str(uuid.uuid4())

    @staticmethod
    def artists():
        result = []
        for _ in range(3):
            new_artist = ArtistFactory.create()
            result.append(new_artist)
        return result

    class Meta:
        model = Album
