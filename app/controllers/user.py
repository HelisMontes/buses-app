from app.decorators.request import request
from app.decorators.response import response
from app.serializers.user import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view


@csrf_exempt
@api_view(['GET'])
@request
@response
def get_all(payload: dict) -> dict:
    '''
    Obtener todos los usuarios

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
            - users: dict
        - message: str
    '''
    query_params = payload.get('query_params')

    page = query_params.get('page', 1)
    per_page = query_params.get('per_page', 10)

    params = {
        'page': page,
        'per_page': per_page,
    }

    if query_params.get('filter_by'):
        params['filter_by'] = query_params.get('filter_by')
        params['filter_value'] = query_params.get('filter_value')
    if query_params.get('sort_by'):
        params['sort_by'] = query_params.get('sort_by')
        params['sort_type'] = query_params.get('sort_type')

    type_user = query_params.get('type_user', '').upper()
    if type_user:
        if type_user not in dict(UserSerializer.TYPE_USER_CHOICES):
            return {
                'message': 'Type user is not valid',
                'status_code': 422,
            }
        params['type_user'] = type_user

    userSerializer = UserSerializer()
    users = userSerializer.get_all(**params)

    return {
        'data': {
            'users': users,
        },
    }


@csrf_exempt
@api_view(['GET'])
@request
@response
def get_one(payload: dict) -> dict:
    '''
    Obtener una usuario

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
            - user: dict
        - message: str
    '''
    path_params = payload.get('path_params')
    pk = path_params.get('pk')

    serializer = UserSerializer()
    user = serializer.get_one(pk)
    if not user:
        return {
            'message': 'User with id {} does not exist'.format(pk),
            'status_code': 404,
        }
    return {
        'data': {
            'user': user.data,
        },
    }


@csrf_exempt
@api_view(['POST'])
@request
@response
def create(payload: dict) -> dict:
    '''
    Crear una usuario

    Parameters
    ----------
    payload : dict
        payload de la petición
        - body: dict
            Datos del usuario

    Returns
    -------
    dict
        - data: dict
            - location: dict
        - message: str
    '''
    body = payload.get('body')

    serializer = UserSerializer(data=body)
    if not serializer.is_valid():
        return {
            'message': serializer.errors,
            'status_code': 422,
        }

    serializer.save()
    return {
        'data': {
            'user': serializer.data,
        },
        'status_code': 201,
    }


@csrf_exempt
@api_view(['POST'])
@request
@response
def update(payload: dict) -> dict:
    '''
    Actualizar un usuario

    Parameters
    ----------
    payload : dict
        payload de la petición
        - body: dict
            Datos del usuario

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
            'message': 'Id is required',
            'status_code': 400,
        }

    pk = body.get('id')

    serializer = UserSerializer()
    user = serializer.get_one(pk)
    if not user:
        return {
            'message': 'User with id {} does not exist'.format(pk),
            'status_code': 404,
        }

    user.set_data(body)
    if not user.is_valid():
        return {
            'message': user.errors,
            'status_code': 422,
        }

    user.save()

    return {
        'data': {
            'user': user.data,
        },
    }


@csrf_exempt
@api_view(['POST'])
@request
@response
def delete(payload: dict) -> dict:
    '''
    Eliminar un usuario

    Parameters
    ----------
    payload : dict
        payload de la petición
        - body: dict
            Datos del usuario
            - id: int
                Primary key del usuario

    Returns
    -------
    dict
        - message: str
    '''
    body = payload.get('body')

    if not body.get('id'):
        return {
            'message': 'Id is required',
            'status_code': 400,
        }

    pk = body.get('id')

    serializer = UserSerializer()
    user = serializer.get_one(pk)
    if not user:
        return {
            'message': 'User with id {} does not exist'.format(pk),
            'status_code': 404,
        }

    user.instance.delete()

    return {
        'message': 'User with id {} has been deleted'.format(pk),
    }
