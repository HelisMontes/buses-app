from app.decorators.response import response
from app.decorators.methods import clean_get
from app.decorators.methods import clean_post
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from app.serializers.location import LocationSerializer


@csrf_exempt
@api_view(['GET'])
@clean_get
@response
def get_all(query_params):
    """Get all buses"""
    page = query_params.get('page', 1)
    per_page = query_params.get('per_page', 10)

    locationSerializer = LocationSerializer()
    locations = locationSerializer.get_all(
        page=page,
        per_page=per_page,
    )

    return {
        'data': {
            'locations': locations.data,
            'meta': {
                'page': page,
                'per_page': per_page,
                'total_items': len(locations.data),
            },
        },
        'message': 'success',
    }


@csrf_exempt
@api_view(['GET'])
@response
def get_one(request, pk):
    serializer = LocationSerializer()
    location = serializer.get_one(pk)
    if not location:
        return {
            'message': 'Location with id {} does not exist'.format(pk),
            'status': 404,
        }
    return {
        'data': {
            'location': location.data,
        },
        'message': 'success',
    }


@csrf_exempt
@api_view(['POST'])
@clean_post
@response
def create(body):
    serializer = LocationSerializer(data=body)
    if not serializer.is_valid():
        return {
            'message': serializer.errors,
            'status': 400,
        }

    serializer.save()
    return {
        'data': {
            'location': serializer.data,
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

    serializer = LocationSerializer()
    location = serializer.get_one(pk)
    if not location:
        return {
            'message': 'Location with id {} does not exist'.format(pk),
            'status': 404,
        }

    location.set_data(body)
    if not location.is_valid():
        return {
            'message': location.errors,
            'status': 422,
        }

    location.save()

    return {
        'data': {
            'location': location.data,
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

    serializer = LocationSerializer()
    location = serializer.get_one(pk)
    if not location:
        return {
            'message': 'Location with id {} does not exist'.format(pk),
            'status': 404,
        }

    location.instance.delete()

    return {
        'message': 'Location with id {} has been deleted'.format(pk),
    }
