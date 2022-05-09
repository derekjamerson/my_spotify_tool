from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    spotify_id = models.CharField(max_length=100, primary_key=True)
