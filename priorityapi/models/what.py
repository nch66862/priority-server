from django.db import models

class What(models.Model):

    priority = models.ForeignKey("Priority", on_delete=models.CASCADE)
    what = models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)

    @property
    def time_on_what(self):
        return self.__time_on_what

    @time_on_what.setter
    def time_on_what(self, value):
        self.__time_on_what = value
