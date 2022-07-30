from app.decorators.request import request
from app.decorators.response import response
from app.serializers.ticket import TicketSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view


@csrf_exempt
@api_view(['GET'])
@request
@response
def get_all(payload: dict) -> dict:
    '''
    Obtener todos los tickets

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
            - tickets: dict
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

    ticketSerializer = TicketSerializer()
    tickets = ticketSerializer.get_all(**params)

    return {
        'data': {
            'tickets': tickets,
        },
    }


@csrf_exempt
@api_view(['GET'])
@request
@response
def get_one(payload: dict) -> dict:
    '''
    Obtener un ticket

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
            - ticket: dict
        - message: str
    '''
    path_params = payload.get('path_params')
    pk = path_params.get('pk')

    serializer = TicketSerializer()
    ticket = serializer.get_one(pk)
    if not ticket:
        return {
            'message': 'Ticket with id {} does not exist'.format(pk),
            'status_code': 404,
        }
    return {
        'data': {
            'ticket': ticket.data,
        },
    }


@csrf_exempt
@api_view(['POST'])
@request
@response
def create(payload: dict) -> dict:
    '''
    Crear un ticket

    Parameters
    ----------
    payload : dict
        payload de la petición
        - body: dict
            Datos del ticket

    Returns
    -------
    dict
        - data: dict
            - ticket: dict
        - message: str
    '''
    body = payload.get('body')
    serializer = TicketSerializer(data=body)
    if not serializer.is_valid():
        return {
            'message': serializer.errors,
            'status_code': 422,
        }

    serializer.save()
    return {
        'data': {
            'ticket': serializer.data,
        },
        'status_code': 201,
    }


@csrf_exempt
@api_view(['POST'])
@request
@response
def update(payload: dict) -> dict:
    '''
    Actualizar un ticket

    Parameters
    ----------
    payload : dict
        payload de la petición
        - body: dict
            Datos del ticket

    Returns
    -------
    dict
        - data: dict
            - ticket: dict
        - message: str
    '''
    body = payload.get('body')
    if not body.get('id'):
        return {
            'message': 'Id is required',
            'status_code': 400,
        }

    pk = body.get('id')

    serializer = TicketSerializer()
    ticket = serializer.get_one(pk)
    if not ticket:
        return {
            'message': 'Ticket with id {} does not exist'.format(pk),
            'status_code': 404,
        }

    ticket.set_data(body)
    if not ticket.is_valid():
        return {
            'message': ticket.errors,
            'status_code': 422,
        }

    ticket.save()

    return {
        'data': {
            'ticket': ticket.data,
        },
    }


@csrf_exempt
@api_view(['POST'])
@request
@response
def delete(payload: dict) -> dict:
    '''
    Eliminar un ticket

    Parameters
    ----------
    payload : dict
        payload de la petición
        - body: dict
            Datos del ticket
            - id: int
                Primary key del ticket

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

    serializer = TicketSerializer()
    ticket = serializer.get_one(pk)
    if not ticket:
        return {
            'message': 'Ticket with id {} does not exist'.format(pk),
            'status_code': 404,
        }

    ticket.instance.delete()

    return {
        'message': 'Ticket with id {} has been deleted'.format(pk),
    }
