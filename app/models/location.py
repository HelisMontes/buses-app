from django.db import models


class Location(models.Model):
    '''
    Modelo de localización

    Attributes
    ----------
    country : str
        País de la localización
    city : str
        Ciudad de la localización
    image : str
        Path de la imagen de la localización
    '''
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    image = models.CharField(max_length=100, blank=True, null=True)

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
