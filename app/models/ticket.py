from django.db import models
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator


class Ticket(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='user_ticket',
    )
    journey = models.ForeignKey(
        'Journey',
        on_delete=models.CASCADE,
        related_name='journey_ticket',
    )
    number_seat = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
