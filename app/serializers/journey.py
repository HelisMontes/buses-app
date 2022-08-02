from datetime import datetime
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Avg
from django.db.models import CharField
from django.db.models import Count
from django.db.models import F
from django.db.models import Value
from django.db.models.functions import Concat
from django.utils import timezone
from rest_framework import serializers

from app.helpers.filter_and_sort import filter_and_sort
from app.helpers.float_decimal_round import float_decimal_round
from app.helpers.pagination import pagination
from app.models.bus import Bus
from app.models.journey import Journey
from app.models.location import Location
from app.models.ticket import Ticket
from app.models.user import User
from app.serializers.bus import BusSerializer
from app.serializers.location import LocationSerializer
from app.serializers.user import UserSerializer
from app.utils.serializer import Serializer


class JourneySerializer(Serializer):
    _model = Journey

    id = serializers.IntegerField(read_only=True)

    origen_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
        required=True,
    )
    origen = LocationSerializer(
        read_only=True,
        required=False,
    )
    destination_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
        required=True,
    )
    destination = LocationSerializer(
        read_only=True,
        required=False,
    )
    bus_id = serializers.PrimaryKeyRelatedField(
        queryset=Bus.objects.all(),
        required=True,
    )
    bus = BusSerializer(
        read_only=True,
        required=False,
    )
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=True,
    )
    user = UserSerializer(
        read_only=True,
        required=False,
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
        origen_id = data.get('origen_id')
        destination_id = data.get('destination_id')
        bus_id = data.get('bus_id')
        user_id = data.get('user_id')
        datetime_start = data.get('datetime_start')
        datetime_end = data.get('datetime_end')

        if origen_id == destination_id:
            raise serializers.ValidationError({
                'origen_id': 'Origen and destination must be different',
                'destination_id': 'Origen and destination must be different',
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

        if not user_id.type_user == 'DRIV':
            raise serializers.ValidationError({
                'user_id': 'User must be a driver',
            })

        errors = {}
        if not bus_id.is_available(datetime_start, datetime_end, self.instance):
            errors['bus_id'] = 'Bus is not available in this time'
        if not user_id.is_available(datetime_start, datetime_end, self.instance):
            errors['user_id'] = 'User is not available in this time'

        if errors.keys():
            raise serializers.ValidationError(errors)

        data['origen_id'] = origen_id.id
        data['destination_id'] = destination_id.id
        data['bus_id'] = bus_id.id
        data['user_id'] = user_id.id

        return data

    def get_one(self, pk):
        try:
            return JourneySerializer(instance=self._model.objects.get(id=pk))
        except self._model.DoesNotExist:
            return False

    def get_all(
        self,
        page=1,
        per_page=10,
        sort_by='id',
        sort_type='asc',
        filter_by=None,
        filter_value=None,
    ):
        data_list = self._model.objects

        filtered_data_list = filter_and_sort(
            sort_by=sort_by,
            sort_type=sort_type,
            filter_by=filter_by,
            filter_value=filter_value,
            data_list=data_list,
            model=self._model,
        )
        return pagination(
            page=page,
            per_page=per_page,
            data_list=filtered_data_list,
            serializer=JourneySerializer,
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

        return pagination(
            page=page,
            per_page=per_page,
            data_list=list(journeys),
        )

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
        buses = {}
        for ticket in tickets:
            if not buses.get(ticket['journey__bus']):
                buses[ticket['journey__bus']] = []
            buses[ticket['journey__bus']] += [ticket['count']]

        buses_filtered = {}
        for bus, value in buses.items():
            average = float_decimal_round((sum(value) / (len(value)*10)) * 100)
            if average > average_sold:
                buses_filtered[bus] = average

        return pagination(
            page=page,
            per_page=per_page,
            data_list=Bus.objects.filter(id__in=buses_filtered.keys()).order_by('id'),
            serializer=BusSerializer,
        )

    def available_for_sale(
        self,
        page: int = 1,
        per_page: int = 10,
        start: datetime = None,
        end: datetime = None,
        origen: Location = None,
        destination: Location = None,
    ):
        journeys = Journey.objects \
            .filter(
                datetime_start__lte=end,
                datetime_end__gte=start,
                origen=origen,
                destination=destination,
            )
        return pagination(
            page=page,
            per_page=per_page,
            data_list=journeys.order_by('id'),
            serializer=JourneySerializer,
        )

    class Meta:
        model = Journey
        fields = ['id', 'datetime_start', 'datetime_end', 'user', 'user_data', 'bus', 'origen', 'destination']
