from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class Serializer(serializers.Serializer):

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
        return self._model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
