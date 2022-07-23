from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from app.models.bus import Bus
from app.helpers.base64_to_file import base64_to_file


class BusSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    brand = serializers.CharField(required=True, max_length=100)
    model = serializers.CharField(required=True, max_length=100)
    color = serializers.CharField(required=True, max_length=50)
    plate = serializers.CharField(
        required=True,
        max_length=10,
        validators=[
            UniqueValidator(queryset=Bus.objects.all()),
        ],
    )
    quantity_seats = serializers.IntegerField(required=True, min_value=1, max_value=10)
    image = serializers.RegexField(r'data:image\/([a-zA-Z]*);base64,([^\"]*)', required=False)
    year = serializers.IntegerField(min_value=1950, max_value=2050)
    status = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate(self, data):
        data['image'] = base64_to_file(data.get('image')) if data.get('image') else None
        return data

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
        try:
            return BusSerializer(instance=Bus.objects.get(id=pk))
        except Bus.DoesNotExist:
            return False

    def get_all(self, page=1, per_page=10):
        return BusSerializer(
            instance=Bus.objects.all().order_by('-id'),
            many=True,
        )

    class Meta:
        model = Bus
        fields = "__all__"
