import random
import uuid

import factory
from tracks.models import Track


# noinspection PyMethodParameters
class TrackFactory(factory.django.DjangoModelFactory):
    @factory.Sequence
    def name(n):
        return str(uuid.uuid4())

    @factory.Sequence
    def spotify_id(n):
        return str(uuid.uuid4())

    @factory.Sequence
    def duration_ms(n):
        return random.randint(1, 999999)

    @factory.Sequence
    def is_explicit(n):
        return random.randint(0, 1)

    @factory.Sequence
    def popularity(n):
        return random.randint(0, 100)

    @factory.post_generation
    def artists(self, create, artists):
        if not create or not artists:
            return

        self.artists.add(*artists)

    class Meta:
        model = Track
