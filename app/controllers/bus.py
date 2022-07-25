from app.decorators.request import request
from app.decorators.response import response
from app.serializers.bus import BusSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view


@csrf_exempt
@api_view(['GET'])
@request
@response
def get_all(payload: dict) -> dict:
    '''
    Obtener todos los buses

    Parameters
    ----------
    payload: dict
        payload de la petición
        - query_params: dict
            - page: int
            - per_page: int

    Returns
    -------
    dict
        - data: dict
            - buses: dict
        - message: str
    '''
    query_params = payload.get('query_params')

    page = query_params.get('page', 1)
    per_page = query_params.get('per_page', 10)

    busSerializer = BusSerializer()
    buses = busSerializer.get_all(
        page=page,
        per_page=per_page,
    )

    return {
        'data': {
            'buses': buses,
        },
        'message': 'success',
    }


@csrf_exempt
@api_view(['GET'])
@request
@response
def get_one(payload: dict) -> dict:
    '''
    Obtener un bus por id

    Parameters
    ----------
    payload : dict
        payload de la petición
        - path_params: dict
            - pk: int
                Primary key del bus

    Returns
    -------
    dict
        - data: dict
            - bus: dict
        - message: str
    '''
    path_params = payload.get('path_params')
    pk = path_params.get('pk')
    serializer = BusSerializer()
    bus = serializer.get_one(pk)
    if not bus:
        return {
            'message': 'Bus with id {} does not exist'.format(pk),
            'status_code': 404,
        }
    return {
        'data': {
            'bus': bus.data,
        },
        'message': 'success',
    }


@csrf_exempt
@api_view(['POST'])
@request
@response
def create(payload: dict) -> dict:
    '''
    Crear un bus

    Parameters
    ----------
    payload : dict
        payload de la petición
        - body: dict
            Datos del bus

    Returns
    -------
    dict
        - data: dict
            - bus: dict
        - message: str
    '''

    body = payload.get('body')
    serializer = BusSerializer(data=body)
    if not serializer.is_valid():
        return {
            'message': serializer.errors,
            'status_code': 400,
        }

    serializer.save()
    return {
        'data': {
            'bus': serializer.data,
        },
        'status_code': 201,
    }


@csrf_exempt
@api_view(['POST'])
@request
@response
def update(payload: dict) -> dict:
    '''
    Actualizar un bus

    Parameters
    ----------
    payload : dict
        payload de la petición
        - body: dict
            Datos del bus

    Returns
    -------
    dict
        - data: dict
            - bus: dict
    '''
    body = payload.get('body')
    if not body.get('id'):
        return {
            'message': 'id is required',
            'status_code': 400,
        }

    pk = body.get('id')

    serializer = BusSerializer()
    bus = serializer.get_one(pk)
    if not bus:
        return {
            'message': 'Bus with id {} does not exist'.format(pk),
            'status_code': 404,
        }

    bus.set_data(body)
    if not bus.is_valid():
        return {
            'message': bus.errors,
            'status_code': 422,
        }

    bus.save()

    return {
        'data': {
            'bus': bus.data,
        },
    }


@csrf_exempt
@api_view(['POST'])
@request
@response
def delete(payload: dict) -> dict:
    '''
    Eliminar un bus

    Parameters
    ----------
    payload : dict
        payload de la petición
        - path_params: dict
            - pk: int
                Primary key del bus

    Returns
    -------
    dict
        - message: str
    '''
    body = payload.get('body')
    if not body.get('id'):
        return {
            'message': 'id is required',
            'status_code': 400,
        }

    pk = body.get('id')

    serializer = BusSerializer()
    bus = serializer.get_one(pk)
    if not bus:
        return {
            'message': 'Bus with id {} does not exist'.format(pk),
            'status_code': 404,
        }

    bus.instance.delete()

    return {
        'message': 'Bus with id {} has been deleted'.format(pk),
    }
