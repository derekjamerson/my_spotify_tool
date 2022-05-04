import uuid

import factory

from users.models import CustomUser


class CustomUserFactory(factory.django.DjangoModelFactory):
    @factory.Sequence
    def username(n):
        return str(uuid.uuid4())

    @factory.Sequence
    def spotify_id(n):
        return str(uuid.uuid4())

    @factory.Sequence
    def email(n):
        return f'{str(uuid.uuid4())}@gmail.com'

    class Meta:
        model = CustomUser
