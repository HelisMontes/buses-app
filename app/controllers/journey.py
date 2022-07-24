from app.decorators.response import response
from app.decorators.methods import clean_get
from app.decorators.methods import clean_post
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from app.serializers.journey import JourneySerializer


@csrf_exempt
@api_view(['GET'])
@clean_get
@response
def get_all(query_params):
    """Get all journeys"""
    page = query_params.get('page', 1)
    per_page = query_params.get('per_page', 10)

    journeySerializer = JourneySerializer()
    journeys = journeySerializer.get_all(
        page=page,
        per_page=per_page,
    )

    return {
        'data': {
            'journeys': journeys.data,
            'meta': {
                'page': page,
                'per_page': per_page,
                'total_items': len(journeys.data),
            },
        },
        'message': 'success',
    }


@csrf_exempt
@api_view(['GET'])
@response
def get_one(request, pk):
    serializer = JourneySerializer()
    journey = serializer.get_one(pk)
    if not journey:
        return {
            'message': 'Journey with id {} does not exist'.format(pk),
            'status': 404,
        }
    return {
        'data': {
            'journey': journey.data,
        },
        'message': 'success',
    }


@csrf_exempt
@api_view(['POST'])
@clean_post
@response
def create(body):
    serializer = JourneySerializer(data=body)
    if not serializer.is_valid():
        return {
            'message': serializer.errors,
            'status': 400,
        }

    serializer.save()
    return {
        'data': {
            'journey': serializer.data,
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

    serializer = JourneySerializer()
    journey = serializer.get_one(pk)
    if not journey:
        return {
            'message': 'Journey with id {} does not exist'.format(pk),
            'status': 404,
        }

    journey.set_data(body)
    if not journey.is_valid():
        return {
            'message': journey.errors,
            'status': 422,
        }

    journey.save()

    return {
        'data': {
            'journey': journey.data,
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

    serializer = JourneySerializer()
    journey = serializer.get_one(pk)
    if not journey:
        return {
            'message': 'Journey with id {} does not exist'.format(pk),
            'status': 404,
        }

    journey.instance.delete()

    return {
        'message': 'Journey with id {} has been deleted'.format(pk),
    }
