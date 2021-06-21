from django.db import models
from django.contrib.auth.models import User


class PriorityUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def subscribed(self):
        return self.__subscribed

    @subscribed.setter
    def subscribed(self, value):
        self.__subscribed = value
