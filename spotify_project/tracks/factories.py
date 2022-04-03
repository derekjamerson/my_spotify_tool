import random
import uuid

import factory

from albums.factories import AlbumFactory
from artists.factories import ArtistFactory
from tracks.models import Track


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
    def artists(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for artist in extracted:
                self.artists.add(artist)

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.groups.add(group)

    class Meta:
        model = Track
