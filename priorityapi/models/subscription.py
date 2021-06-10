from django.db import models
from django.utils import timezone

class Subscription(models.Model):

    creator = models.ForeignKey("PriorityUser", related_name="creator", on_delete=models.CASCADE)
    subscriber = models.ForeignKey("PriorityUser", related_name="subscriber", on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    ended_on = models.DateTimeField(null=True)
