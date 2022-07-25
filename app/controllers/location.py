from app.decorators.request import request
from app.decorators.response import response
from app.serializers.location import LocationSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view


@csrf_exempt
@api_view(['GET'])
@request
@response
def get_all(payload: dict) -> dict:
    '''
    Obtener todos las localizaciones

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
            - locations: dict
        - message: str
    '''
    query_params = payload.get('query_params')
    page = query_params.get('page', 1)
    per_page = query_params.get('per_page', 10)

    locationSerializer = LocationSerializer()
    locations = locationSerializer.get_all(
        page=page,
        per_page=per_page,
    )

    return {
        'data': {
            'locations': locations,
        },
        'message': 'success',
    }


@csrf_exempt
@api_view(['GET'])
@request
@response
def get_one(payload: dict) -> dict:
    '''
    Obtener una localización

    Parameters
    ----------
    payload : dict
        payload de la petición
        - path_params: dict
            - pk: int
                Primary key de la localización

    Returns
    -------
    dict
        - data: dict
            - location: dict
        - message: str
    '''
    pk = payload.path_params.get('pk')

    serializer = LocationSerializer()
    location = serializer.get_one(pk)
    if not location:
        return {
            'message': 'Location with id {} does not exist'.format(pk),
            'status_code': 404,
        }
    return {
        'data': {
            'location': location.data,
        },
        'message': 'success',
    }


@csrf_exempt
@api_view(['POST'])
@request
@response
def create(payload: dict) -> dict:
    '''
    Crear una localización

    Parameters
    ----------
    payload : dict
        payload de la petición
        - body: dict
            Datos de la localización

    Returns
    -------
    dict
        - data: dict
            - location: dict
        - message: str
    '''
    body = payload.get('body')

    serializer = LocationSerializer(data=body)
    if not serializer.is_valid():
        return {
            'message': serializer.errors,
            'status_code': 400,
        }

    serializer.save()
    return {
        'data': {
            'location': serializer.data,
        },
        'status_code': 201,
    }


@csrf_exempt
@api_view(['POST'])
@request
@response
def update(payload: dict) -> dict:
    '''
    Actualizar una localización

    Parameters
    ----------
    payload : dict
        payload de la petición
        - body: dict
            Datos de la localización

    Returns
    -------
    dict
        - data: dict
            - location: dict
        - message: str
    '''
    body = payload.get('body')

    if not body.get('id'):
        return {
            'message': 'id is required',
            'status_code': 400,
        }

    pk = body.get('id')

    serializer = LocationSerializer()
    location = serializer.get_one(pk)
    if not location:
        return {
            'message': 'Location with id {} does not exist'.format(pk),
            'status_code': 404,
        }

    location.set_data(body)
    if not location.is_valid():
        return {
            'message': location.errors,
            'status_code': 422,
        }

    location.save()

    return {
        'data': {
            'location': location.data,
        },
    }


@csrf_exempt
@api_view(['POST'])
@request
@response
def delete(payload: dict) -> dict:
    '''
    Eliminar una localización

    Parameters
    ----------
    payload : dict
        payload de la petición
        - body: dict
            Datos de la localización
            - id: int
                Primary key de la localización

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

    serializer = LocationSerializer()
    location = serializer.get_one(pk)
    if not location:
        return {
            'message': 'Location with id {} does not exist'.format(pk),
            'status_code': 404,
        }

    location.instance.delete()

    return {
        'message': 'Location with id {} has been deleted'.format(pk),
    }
