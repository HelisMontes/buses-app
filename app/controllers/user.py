from app.decorators.response import response
from app.decorators.methods import clean_get
from app.decorators.methods import clean_post
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from app.serializers.user import UserSerializer


@csrf_exempt
@api_view(['GET'])
@clean_get
@response
def get_all(query_params):
    """Get all users"""
    page = query_params.get('page', 1)
    per_page = query_params.get('per_page', 10)

    userSerializer = UserSerializer()
    users = userSerializer.get_all(
        page=page,
        per_page=per_page,
    )

    return {
        'data': {
            'users': users.data,
            'meta': {
                'page': page,
                'per_page': per_page,
                'total_items': len(users.data),
            },
        },
        'message': 'success',
    }


@csrf_exempt
@api_view(['GET'])
@response
def get_one(request, pk):
    serializer = UserSerializer()
    user = serializer.get_one(pk)
    if not user:
        return {
            'message': 'User with id {} does not exist'.format(pk),
            'status': 404,
        }
    return {
        'data': {
            'user': user.data,
        },
        'message': 'success',
    }


@csrf_exempt
@api_view(['POST'])
@clean_post
@response
def create(body):
    serializer = UserSerializer(data=body)
    if not serializer.is_valid():
        return {
            'message': serializer.errors,
            'status': 400,
        }

    serializer.save()
    return {
        'data': {
            'user': serializer.data,
        },
        'status': 201,
    }


@csrf_exempt
@api_view(['POST'])
@clean_post
@response
def update(body):
    if not body.get('id'):
        return {
            'message': 'id is required',
            'status': 400,
        }

    pk = body.get('id')

    serializer = UserSerializer()
    user = serializer.get_one(pk)
    if not user:
        return {
            'message': 'User with id {} does not exist'.format(pk),
            'status': 404,
        }

    user.set_data(body)
    if not user.is_valid():
        return {
            'message': user.errors,
            'status': 422,
        }

    user.save()

    return {
        'data': {
            'user': user.data,
        },
    }


@csrf_exempt
@api_view(['POST'])
@clean_post
@response
def delete(body):
    if not body.get('id'):
        return {
            'message': 'id is required',
            'status': 400,
        }

    pk = body.get('id')

    serializer = UserSerializer()
    user = serializer.get_one(pk)
    if not user:
        return {
            'message': 'User with id {} does not exist'.format(pk),
            'status': 404,
        }

    user.instance.delete()

    return {
        'message': 'User with id {} has been deleted'.format(pk),
    }
