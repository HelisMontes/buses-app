from django.db import models
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator


class Bus(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    plate = models.CharField(max_length=10, unique=True)
    quantity_seats = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )
    image = models.CharField(max_length=100, blank=True, null=True)
    year = models.PositiveSmallIntegerField()
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
