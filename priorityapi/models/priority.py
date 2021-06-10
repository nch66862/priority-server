from django.db import models
from django.utils import timezone

class Priority(models.Model):

    priority_user = models.ForeignKey("PriorityUser", on_delete=models.CASCADE)
    priority = models.CharField(max_length=200)
    why = models.CharField(max_length=200)
    how = models.IntegerField()
    is_public = models.BooleanField(default=False)
    creation_date = models.DateTimeField(default=timezone.now)