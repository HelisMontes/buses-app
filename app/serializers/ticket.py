from rest_framework import serializers

from app.helpers.filter_and_sort import filter_and_sort
from app.helpers.pagination import pagination
from app.models.journey import Journey
from app.models.ticket import Ticket
from app.models.user import User
from app.utils.serializer import Serializer


class TicketSerializer(Serializer):
    _model = Ticket

    id = serializers.IntegerField(read_only=True)

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=True,
    )
    journey = serializers.PrimaryKeyRelatedField(
        queryset=Journey.objects.all(),
        required=True,
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
        user = data.get('user')
        if not user.type_user == 'PASS':
            raise serializers.ValidationError({
                'user': 'User is not passenger'
            })
        journey = data.get('journey')
        if not journey.status:
            raise serializers.ValidationError({
                'journey': 'Journey is not active'
            })
        if not journey.seat_available(data.get('number_seat'), self.instance):
            raise serializers.ValidationError({
                'number_seat': 'Seat is not available'
            })

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

    class Meta:
        model = Ticket
        fields = '__all__'
