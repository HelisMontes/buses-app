from django.db import models
from app.models.journey import Journey


class User(models.Model):
    '''
    Modelo de usuario

    Attributes
    ----------
    TYPE_USER_CHOICES : tuple
        Tipos de usuario

    identification : str
        Identificación del usuario
    name : str
        Nombre del usuario
    last_name : str
        Apellido del usuario
    email : str
        Correo electrónico del usuario
    phone : str
        Teléfono del usuario
    birth_date : date
        Fecha de nacimiento del usuario
    type_user : str
        Tipo de usuario
    image : str
        Path de la imagen del usuario

    Methods
    -------
    is_available
        Verifica si el usuario está disponible para una fecha y hora
    '''
    TYPE_USER_CHOICES = [
        ('PASS', 'passenger'),
        ('DRIV', 'driver'),
    ]

    identification = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    birth_date = models.DateField()
    type_user = models.CharField(
        max_length=4,
        choices=TYPE_USER_CHOICES,
        default='PASS',
    )
    image = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    def is_available(self, datetime_start, datetime_end, instance=None):
        journeys = Journey.objects.filter(
            user=self,
            datetime_start__lte=datetime_end,
            datetime_end__gte=datetime_start,
        )
        if instance:
            journeys = journeys.exclude(id=instance.id)
        return not journeys.exists()
