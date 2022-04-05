from django.db import models
from django.db.models import CASCADE

import users.models


class Library(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(users.models.CustomUser, on_delete=CASCADE, related_name='library')
    