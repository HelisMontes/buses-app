from django.db import models
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from app.models.journey import Journey


class Bus(models.Model):
    '''
    Modelo de bus

    Attributes
    ----------
    brand : str
        Marca del bus
    model : str
        Modelo del bus
    color : str
        Color del bus
    plate : str
        Placa del bus
    quantity_seats : int
        Cantidad de asientos del bus
    image : str
        Path de la imagen del bus
    year : int
        Año de fabricación del bus

    Methods
    -------
    is_available
        Verifica si el bus está disponible para una fecha y hora
    '''
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

    def is_available(self, datetime_start, datetime_end, instance=None):
        journeys = Journey.objects.filter(
            bus=self,
            datetime_start__lte=datetime_end,
            datetime_end__gte=datetime_start,
        )
        if instance:
            journeys = journeys.exclude(id=instance.id)
        return not journeys.exists()
