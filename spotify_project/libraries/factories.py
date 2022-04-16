import factory
from artists.factories import ArtistFactory
from libraries.models import Library

# noinspection PyMethodParameters
from tracks.factories import TrackFactory
from users.factories import CustomUserFactory


class LibraryFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(CustomUserFactory)

    @factory.post_generation
    def tracks(self, create, tracks):
        if not create:
            return
        if not tracks:
            self.tracks.add(*TrackFactory.create_batch(2))
        else:
            self.tracks.add(*tracks)

    @factory.post_generation
    def artists(self, create, artists):
        if not create:
            return
        if not artists:
            self.artists.add(*ArtistFactory.create_batch(2))
        else:
            self.artists.add(*artists)

    class Meta:
        model = Library
