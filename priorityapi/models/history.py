from django.db import models
from django.utils import timezone

class History(models.Model):

    what = models.ForeignKey("What", on_delete=models.CASCADE)
    submission_date = models.DateTimeField(default=timezone.now)
    goal_date = models.DateField()
    time_spent = models.IntegerField()

    @property
    def week_total(self):
        return self.__week_total

    @week_total.setter
    def week_total(self, value):
        self.__week_total = value
