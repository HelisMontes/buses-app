from email.policy import default
from django.db import models


class Location(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
