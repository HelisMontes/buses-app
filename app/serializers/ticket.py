from rest_framework import serializers

from app.helpers.filter_and_sort import filter_and_sort
from app.helpers.pagination import pagination
from app.models.ticket import Ticket
from app.models.journey import Journey
from app.models.user import User
from app.utils.serializer import Serializer
from app.serializers.journey import JourneySerializer
from app.serializers.user import UserSerializer


class TicketSerializer(Serializer):
    _model = Ticket

    id = serializers.IntegerField(read_only=True)

    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=True,
    )
    user = UserSerializer(
        read_only=True,
        required=False,
    )

    journey_id = serializers.PrimaryKeyRelatedField(
        queryset=Journey.objects.all(),
        required=True,
    )
    journey = JourneySerializer(
        read_only=True,
        required=False,
    )

    number_seat = serializers.IntegerField(
        min_value=1,
        max_value=10,
        required=True,
    )

    status = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate(self, data):
        user_id = data.get('user_id')
        if not user_id.type_user == 'PASS':
            raise serializers.ValidationError({
                'user': 'User is not passenger'
            })
        journey_id = data.get('journey_id')
        if not journey_id.status:
            raise serializers.ValidationError({
                'journey': 'Journey is not active'
            })
        if not journey_id.seat_available(data.get('number_seat'), self.instance):
            raise serializers.ValidationError({
                'number_seat': 'Seat is not available'
            })

        data['user_id'] = user_id.id
        data['journey_id'] = journey_id.id

        return data

    def get_one(self, pk):
        try:
            return TicketSerializer(instance=self._model.objects.get(id=pk))
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
            serializer=TicketSerializer,
        )

    def to_buy(self, journey):
        tickets = TicketSerializer(
            instance=self._model.objects.filter(
                journey=journey,
                status=True,
            ),
            many=True,
        )
        return tickets

    class Meta:
        model = Ticket
        fields = '__all__'
