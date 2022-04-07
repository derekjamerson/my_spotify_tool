import uuid

import factory
from artists.models import Artist


# noinspection PyMethodParameters
class ArtistFactory(factory.django.DjangoModelFactory):
    @factory.Sequence
    def name(n):
        return str(uuid.uuid4())

    @factory.Sequence
    def spotify_id(n):
        return str(uuid.uuid4())

    class Meta:
        model = Artist
