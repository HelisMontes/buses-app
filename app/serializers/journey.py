from rest_framework import serializers
from django.utils import timezone
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Value, CharField, Count, F, IntegerField, Sum, Avg
from django.db.models.functions import Concat

from app.models.journey import Journey
from app.models.ticket import Ticket
from app.models.location import Location
from app.models.user import User
from app.models.bus import Bus
from app.serializers.bus import BusSerializer
from app.utils.serializer import Serializer
from app.helpers.float_decimal_round import float_decimal_round


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
        if not bus.is_available(datetime_start, datetime_end, self.instance):
            errors['bus'] = 'Bus is not available in this time'
        if not user.is_available(datetime_start, datetime_end, self.instance):
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

    def average_passengers(self, page=1, per_page=10):
        journeys = self._model.objects \
            .values(
                'origen',
                'destination',
            ) \
            .annotate(
                ids=ArrayAgg('id'),
                range=Avg(
                    F('datetime_end') - F('datetime_start'),
                ),
                name=Concat(
                    'origen__country',
                    Value('-'),
                    'origen__city',
                    Value(' / '),
                    'destination__country',
                    Value('-'),
                    'destination__city',
                    output_field=CharField(),
                ),
            )

        journeys_ids = sum([journey['ids'] for journey in journeys], [])

        tickets = Ticket.objects \
            .values(
                'journey__id',
            ) \
            .filter(
                journey__id__in=journeys_ids,
            ) \
            .annotate(
                passengers=Count('id'),
            )
        for ticket in tickets:
            for journey in journeys:
                if ticket['journey__id'] in journey['ids']:
                    if not journey.get('passengers'):
                        journey['passengers'] = []
                    journey['passengers'] += [ticket['passengers']]
        for journey in journeys:
            if not journey.get('passengers'):
                journey['passengers'] = []
            journey['passengers_average'] = float_decimal_round(
                sum(journey['passengers']) / len(journey['passengers'])
            )
            if journey.get('range'):
                journey['range'] = journey['range'].total_seconds()
            del journey['passengers']
            del journey['ids']
            del journey['origen']
            del journey['destination']

        return list(journeys)[(page - 1) * per_page:page * per_page]

    def buses_average_sold(
        self,
        page=1,
        per_page=10,
        average_sold=0,
        journey=None,
    ):
        tickets = Ticket.objects \
            .values(
                'journey__id',
                'journey__bus',
            ) \
            .filter(
                journey__origen=journey.origen,
                journey__destination=journey.destination,
            ) \
            .annotate(
                count=Count('id'),
            )
        print('tickets', tickets)
        buses = {}
        for ticket in tickets:
            if not buses.get(ticket['journey__bus']):
                buses[ticket['journey__bus']] = []
            buses[ticket['journey__bus']] += [ticket['count']]
        print('buses', buses)

        buses_filtered = {}
        for bus, value in buses.items():
            average = float_decimal_round((sum(value) / (len(value)*10)) * 100)
            print('average', average)
            if average > average_sold:
                buses_filtered[bus] = average

        return BusSerializer(
            instance=Bus.objects.filter(id__in=buses_filtered.keys()).order_by('id')[(page - 1) * per_page:page * per_page],
            many=True,
        )

    class Meta:
        model = Journey
        fields = '__all__'
