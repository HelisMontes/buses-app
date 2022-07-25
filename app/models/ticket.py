from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models


class Ticket(models.Model):
    '''
    Modelo de ticket

    Attributes
    ----------
    user : int
        Id del usuario
    journey : int
        Id del viaje
    number_seat : int
        Numero de asiento
    '''
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
