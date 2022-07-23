from app.decorators.response import response
from app.decorators.methods import clean_get
from app.decorators.methods import clean_post
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from app.serializers.bus import BusSerializer


@csrf_exempt
@api_view(['GET'])
@clean_get
@response
def get_all(query_params):
    """Get all buses"""
    page = query_params.get('page', 1)
    per_page = query_params.get('per_page', 10)

    busSerializer = BusSerializer()
    buses = busSerializer.get_all(
        page=page,
        per_page=per_page,
    )

    return {
        'data': {
            'buses': buses.data,
            'meta': {
                'page': page,
                'per_page': per_page,
                'total_items': len(buses.data),
            },
        },
        'message': 'success',
    }


@csrf_exempt
@api_view(['GET'])
@response
def get_one(request, pk):
    serializer = BusSerializer()
    bus = serializer.get_one(pk)
    if not bus:
        return {
            'message': 'Bus with id {} does not exist'.format(pk),
            'status': 404,
        }
    return {
        'data': {
            'bus': bus.data,
        },
        'message': 'success',
    }


@csrf_exempt
@api_view(['POST'])
@clean_post
@response
def create(body):
    serializer = BusSerializer(data=body)
    if not serializer.is_valid():
        return {
            'message': serializer.errors,
            'status': 400,
        }

    serializer.save()
    return {
        'data': {
            'bus': serializer.data,
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

    serializer = BusSerializer()
    bus = serializer.get_one(pk)
    if not bus:
        return {
            'message': 'Bus with id {} does not exist'.format(pk),
            'status': 404,
        }

    bus.initial_data = body
    if not bus.is_valid():
        return {
            'message': bus.errors,
            'status': 422,
        }

    bus.save()

    return {
        'data': {
            'bus': bus.data,
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

    serializer = BusSerializer()
    bus = serializer.get_one(pk)
    if not bus:
        return {
            'message': 'Bus with id {} does not exist'.format(pk),
            'status': 404,
        }

    bus.delete()

    return {
        'message': 'Bus with id {} has been deleted'.format(pk),
    }
