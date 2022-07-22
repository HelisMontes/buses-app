from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from app.models.bus import Bus


class BusSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    brand = serializers.CharField(required=True, max_length=100)
    model = serializers.CharField(required=True, max_length=100)
    color = serializers.CharField(required=True, max_length=50)
    plate = serializers.CharField(
        required=True,
        max_length=10,
        validators=[UniqueValidator(queryset=Bus.objects.all())]
    )
    quantity_seats = serializers.IntegerField(required=True, min_value=1, max_value=10)
    year = serializers.IntegerField(min_value=1950, max_value=2050)
    status = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Bus.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.brand = validated_data.get('brand', instance.brand)
        instance.model = validated_data.get('model', instance.model)
        instance.color = validated_data.get('color', instance.color)
        instance.plate = validated_data.get('plate', instance.plate)
        instance.quantity_seats = validated_data.get('quantity_seats', instance.quantity_seats)
        instance.year = validated_data.get('year', instance.year)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

    def get_one(self, pk):
        response = {
            'data': {},
            'message': '',
            'is_valid': False,
        }
        try:
            response['data'] = BusSerializer(Bus.objects.get(pk=pk))
            response['message'] = 'Bus found'
            response['is_valid'] = True
        except Bus.DoesNotExist:
            response['message'] = 'Bus not found'
        return response

    class Meta:
        model = Bus
        fields = "__all__"
