from rest_framework import serializers
from django.utils import timezone

from app.models.journey import Journey
from app.models.location import Location
from app.models.user import User
from app.models.bus import Bus
from app.utils.serializer import Serializer


class JourneySerializer(Serializer):
    _model = Journey

    id = serializers.IntegerField(read_only=True)

    origen = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
        required=True,
    )
    destination = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
        required=True,
    )
    bus = serializers.PrimaryKeyRelatedField(
        queryset=Bus.objects.all(),
        required=True,
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=True,
    )

    price = serializers.DecimalField(
        required=True,
        max_digits=10,
        decimal_places=2,
    )

    datetime_start = serializers.DateTimeField()
    datetime_end = serializers.DateTimeField()

    status = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate(self, data):
        origen = data.get('origen')
        destination = data.get('destination')
        bus = data.get('bus')
        user = data.get('user')
        datetime_start = data.get('datetime_start')
        datetime_end = data.get('datetime_end')

        if origen == destination:
            raise serializers.ValidationError({
                'origen': 'Origen and destination must be different',
                'destination': 'Origen and destination must be different',
            })

        if datetime_start < timezone.now():
            raise serializers.ValidationError({
                'datetime_start': 'Datetime start must be greater than now',
            })
        if datetime_end < timezone.now():
            raise serializers.ValidationError({
                'datetime_end': 'Datetime end must be greater than now',
            })
        if datetime_end < datetime_start:
            raise serializers.ValidationError({
                'datetime_end': 'Datetime end must be greater than datetime start',
            })

        if not user.type_user == 'DRIV':
            raise serializers.ValidationError({
                'user': 'User must be a driver',
            })

        errors = {}
        if not bus.is_available(datetime_start, datetime_end):
            errors['bus'] = 'Bus is not available in this time'
        if not user.is_available(datetime_start, datetime_end):
            errors['user'] = 'User is not available in this time'

        if errors.keys():
            raise serializers.ValidationError(errors)

        return data

    def get_one(self, pk):
        try:
            return JourneySerializer(instance=self._model.objects.get(id=pk))
        except self._model.DoesNotExist:
            return False

    def get_all(self, page=1, per_page=10):
        return JourneySerializer(
            instance=self._model.objects.all().order_by('id')[(page - 1) * per_page:page * per_page],
            many=True,
        )

    class Meta:
        model = Journey
        fields = '__all__'
