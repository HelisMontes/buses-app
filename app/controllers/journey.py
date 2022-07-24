from app.decorators.response import response
from app.decorators.request import request
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from app.serializers.journey import JourneySerializer


@csrf_exempt
@api_view(['GET'])
@request
@response
def get_all(payload: dict) -> dict:
    '''
    Obtener todos las rutas

    Parameters
    ----------
    payload : dict
        payload de la petición
        - query_params: dict
            - page: int
            - per_page: int

    Returns
    -------
    dict
        - data: dict
            - journeys: list
                - dict
            - meta: dict
                - page: int
                - per_page: int
                - total_items: int
        - message: str
    '''
    query_params = payload.get('query_params')

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
@request
@response
def get_one(payload: dict) -> dict:
    '''
    Obtener una ruta

    Parameters
    ----------
    payload : dict
        payload de la petición
        - path_params: dict
            - pk: int

    Returns
    -------
    dict
        - data: dict
            - journey: dict
        - message: str
    '''
    path_params = payload.get('path_params')
    pk = path_params.get('pk')

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
@request
@response
def create(payload: dict) -> dict:
    '''
    Crear una ruta

    Parameters
    ----------
    payload : dict
        payload de la petición
        - body: dict
            Datos de la ruta

    Returns
    -------
    dict
        - data: dict
            - journey: dict
        - message: str
    '''
    body = payload.get('body')
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
@request
@response
def update(payload: dict) -> dict:
    '''
    Actualizar una ruta

    Parameters
    ----------
    payload : dict
        payload de la petición
        - body: dict
            Datos de la ruta

    Returns
    -------
    dict
        - data: dict
            - journey: dict
        - message: str
    '''
    body = payload.get('body')

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
@request
@response
def delete(payload: dict) -> dict:
    '''
    Eliminar una ruta

    Parameters
    ----------
    payload : dict
        payload de la petición
        - body: dict
            Datos de la ruta
            - id: int
                Primary key de la ruta

    Returns
    -------
    dict
        - message: str
    '''
    body = payload.get('body')

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


@csrf_exempt
@api_view(['GET'])
@request
@response
def average_passengers(payload: dict) -> dict:
    '''
    Obtener el promedio de pasajeros por ruta

    Parameters
    ----------
    payload : dict
        payload de la petición
        - query_params: dict
            - page: int
            - per_page: int

    Returns
    -------
    dict
        - data: dict
            - journeys: list
                - dict
            - meta: dict
                - page: int
                - per_page: int
                - total_items: int
        - message: str
    '''
    query_params = payload.get('query_params')

    page = query_params.get('page', 1)
    per_page = query_params.get('per_page', 10)

    journeySerializer = JourneySerializer()
    journeys = journeySerializer.average_passengers(
        page=page,
        per_page=per_page,
    )

    return {
        'data': {
            'journeys': journeys,
            'meta': {
                'page': page,
                'per_page': per_page,
            },
        },
        'message': 'success',
    }
