from django.db import models
from django.utils import timezone

class Affirmation(models.Model):

    priority_user = models.ForeignKey("PriorityUser", on_delete=models.CASCADE)
    priority = models.ForeignKey("Priority", on_delete=models.CASCADE)
    affirmation = models.CharField(max_length=200)
    created_on = models.DateTimeField(default=timezone.now)

    @property
    def is_author(self):
        return self.__is_author

    @is_author.setter
    def is_author(self, value):
        self.__is_author = value

