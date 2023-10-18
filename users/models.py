from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    total_reading_time_week = models.DurationField(null=True, blank=True)
    total_reading_time_month = models.DurationField(null=True, blank=True)
