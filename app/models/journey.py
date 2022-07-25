from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models

from app.models.ticket import Ticket


class Journey(models.Model):
    '''
    Modelo de viaje

    Attributes
    ----------
    origen : int
        Id de la localización de origen
    destino : int
        Id de la localización de destino
    bus : int
        Id del bus
    user : int
        Id del usuario
    datetime_start : datetime
        Fecha y hora de inicio del viaje
    datetime_end : datetime
        Fecha y hora de fin del viaje
    price : float
        Precio del viaje

    Methods
    -------
    seat_available
        Verifica si el asiento está disponible para una fecha y hora
    '''
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

    def seat_available(self, number_seat, instance=None):
        ticket = Ticket.objects.filter(
            journey=self,
            status=True,
            number_seat=number_seat,
        )
        if instance:
            ticket = ticket.exclude(id=instance.id)
        return not ticket.exists()
