import factory
from libraries.models import Library

# noinspection PyMethodParameters
from users.factories import CustomUserFactory


class LibraryFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(CustomUserFactory)

    @factory.post_generation
    def tracks(self, create, tracks):
        if not create or not tracks:
            return

        self.tracks.add(*tracks)

    @factory.post_generation
    def artists(self, create, artists):
        if not create or not artists:
            return

        self.artists.set(artists)

    class Meta:
        model = Library
