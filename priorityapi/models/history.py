from django.db import models
from django.utils import timezone

class History(models.Model):

    what = models.ForeignKey("What", on_delete=models.CASCADE)
    submission_date = models.DateTimeField(default=timezone.now)
    goal_date = models.DateField()
    time_spent = models.IntegerField()