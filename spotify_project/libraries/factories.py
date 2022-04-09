import uuid

import factory
from libraries.models import Library
from users.models import CustomUser


# noinspection PyMethodParameters
class LibraryFactory(factory.django.DjangoModelFactory):
    @factory.post_generation
    def tracks(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.tracks.add(*extracted)

    @factory.post_generation
    def artists(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.artists.add(*extracted)

    class Meta:
        model = Library
