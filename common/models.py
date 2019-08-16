from django.db import models
from django.conf import settings
from user.models import User


class OnlineUsersTrackingModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_active_time = models.DateTimeField()
