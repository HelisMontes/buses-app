from django.db import models
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator


class Journey(models.Model):
    origen = models.ForeignKey(
        'Location',
        on_delete=models.CASCADE,
        related_name='origen_journey',
    )
    destination = models.ForeignKey(
        'Location',
        on_delete=models.CASCADE,
        related_name='destination_journey',
    )
    bus = models.ForeignKey(
        'Bus',
        on_delete=models.CASCADE,
        related_name='bus_journey',
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='user_journey',
    )
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()

    price = models.FloatField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(1000),
        ]
    )

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
