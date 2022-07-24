from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from app.models.location import Location
from app.helpers.validate_base64_image import validate_base64_image
from app.helpers.save_image import save_image
from app.helpers.verify_image_exists import verify_image_exists
from app.utils.serializer import Serializer


class LocationSerializer(Serializer):
    _model = Location

    id = serializers.IntegerField(read_only=True)
    country = serializers.CharField(required=True, max_length=100)
    city = serializers.CharField(required=True, max_length=100)
    image = serializers.CharField(required=False, allow_blank=True)
    status = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate(self, data):
        if data.get('image'):
            data_image = data.get('image')
            if self.instance:
                if validate_base64_image(data_image):
                    data['image'] = save_image(data_image, self._model)
                elif verify_image_exists(data_image):
                    data['image'] = data_image
                elif data_image == 'delete':
                    data['image'] = None
                else:
                    raise serializers.ValidationError({
                        'image': 'Image is not valid'
                    })
            else:
                if validate_base64_image(data_image):
                    data['image'] = save_image(data_image, self._model)
                else:
                    raise serializers.ValidationError({
                        'image': 'Image is not valid'
                    })
        return data

    def get_one(self, pk):
        try:
            return LocationSerializer(instance=self._model.objects.get(id=pk))
        except self._model.DoesNotExist:
            return False

    def get_all(self, page=1, per_page=10):
        return LocationSerializer(
            instance=self._model.objects.all().order_by('id')[(page - 1) * per_page:page * per_page],
            many=True,
        )

    class Meta:
        model = Location
        fields = "__all__"

        validators = [
            UniqueTogetherValidator(
                queryset=Location.objects.all(),
                fields=['country', 'city']
            )
        ]
