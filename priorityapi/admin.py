from django.contrib import admin
from .models import Affirmation, History, PriorityUser, Priority, Subscription, What
# Register your models here.

admin.site.register(Affirmation)
admin.site.register(History)
admin.site.register(PriorityUser)
admin.site.register(Priority)
admin.site.register(Subscription)
admin.site.register(What)