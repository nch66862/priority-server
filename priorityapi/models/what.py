from django.db import models

class What(models.Model):

    priority = models.ForeignKey("Priority", on_delete=models.CASCADE)
    what = models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)
