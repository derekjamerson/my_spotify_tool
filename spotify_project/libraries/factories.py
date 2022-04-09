import uuid

import factory
from libraries.models import Library
from users.models import CustomUser


# noinspection PyMethodParameters
class LibraryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Library
