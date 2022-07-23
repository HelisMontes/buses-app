from django.db import models


class User(models.Model):
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
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
