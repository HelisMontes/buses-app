from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from app.models.user import User
from app.helpers.validate_base64_image import validate_base64_image
from app.helpers.save_image import save_image
from app.helpers.verify_image_exists import verify_image_exists
from app.helpers.pagination import pagination
from app.helpers.filter_and_sort import filter_and_sort
from app.utils.serializer import Serializer


class UserSerializer(Serializer):
    _model = User

    TYPE_USER_CHOICES = User.TYPE_USER_CHOICES

    id = serializers.IntegerField(read_only=True)
    identification = serializers.CharField(
        required=True,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField(
        required=True,
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    phone = serializers.CharField(
        required=True,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    birth_date = serializers.DateField()
    type_user = serializers.ChoiceField(
        choices=User.TYPE_USER_CHOICES,
    )
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
            return UserSerializer(instance=self._model.objects.get(id=pk))
        except self._model.DoesNotExist:
            return False

    def get_all(
        self,
        page=1,
        per_page=10,
        type_user=None,
        sort_by='id',
        sort_type='asc',
        filter_by=None,
        filter_value=None,
    ):
        data_list = self._model.objects
        if type_user:
            data_list = data_list.filter(type_user=type_user)

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
            serializer=UserSerializer,
        )

    class Meta:
        model = User
        fields = '__all__'
