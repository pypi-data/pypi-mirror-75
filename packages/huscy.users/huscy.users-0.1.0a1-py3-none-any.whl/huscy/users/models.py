from enum import Enum

from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    class LANGUAGE(Enum):
        de = ('de', 'Deutsch')
        en = ('en', 'English')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    prefered_language = models.CharField(max_length=2, choices=[x.value for x in LANGUAGE],
                                         default='en')
