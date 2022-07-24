from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils import timezone


class Serializer(serializers.Serializer):
    '''
    Clase base para los serializers

    Attributes
    ----------

    Methods
    -------
    set_data
        Setea los datos del serializer

    create
        Crea un nuevo registro

    update
        Actualiza un registro
    '''

    def set_data(self, data):
        if not self.instance:
            raise ValidationError('Instance is not set')
        data_old = self.instance.__dict__
        data_new = {
            **data_old,
            **data,
        }
        data_cleaned = {
            key: value for key, value in data_new.items() if value is not None
        }
        self.initial_data = data_cleaned

    def create(self, validated_data):
        validated_data['created_at'] = timezone.now()
        return self._model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.updated_at = timezone.now()
        instance.save()
        return instance
