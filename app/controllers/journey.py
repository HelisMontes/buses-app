from app.decorators.request import request
from app.decorators.response import response
from app.serializers.journey import JourneySerializer
from app.serializers.location import LocationSerializer
from app.serializers.ticket import TicketSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from app.helpers.validate_datetime import validate_datetime


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
            - journeys: dict
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

    journeySerializer = JourneySerializer()
    journeys = journeySerializer.get_all(**params)

    return {
        'data': {
            'journeys': journeys,
        },
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
            'status_code': 404,
        }
    return {
        'data': {
            'journey': journey.data,
        },
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
            'status_code': 422,
        }

    serializer.save()
    return {
        'data': {
            'journey': serializer.data,
        },
        'status_code': 201,
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
            'message': 'Id is required',
            'status_code': 400,
        }

    pk = body.get('id')

    serializer = JourneySerializer()
    journey = serializer.get_one(pk)
    if not journey:
        return {
            'message': 'Journey with id {} does not exist'.format(pk),
            'status_code': 404,
        }

    journey.set_data(body)
    if not journey.is_valid():
        return {
            'message': journey.errors,
            'status_code': 422,
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
            'message': 'Id is required',
            'status_code': 400,
        }

    pk = body.get('id')

    serializer = JourneySerializer()
    journey = serializer.get_one(pk)
    if not journey:
        return {
            'message': 'Journey with id {} does not exist'.format(pk),
            'status_code': 404,
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
        },
    }


@csrf_exempt
@api_view(['GET'])
@request
@response
def buses_average_sold(payload: dict) -> dict:
    '''
    Obtener el promedio de buses vendidos por ruta

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

    average_sold = query_params.get('average_sold')
    if not average_sold:
        return {
            'message': 'average_sold is required',
            'status_code': 422,
        }
    if not average_sold.isdigit():
        return {
            'message': 'average_sold must be a number',
            'status_code': 422,
        }
    average_sold = float(average_sold)

    if average_sold < 0:
        return {
            'message': 'average_sold must be greater than 0',
            'status_code': 422,
        }
    if average_sold > 100:
        return {
            'message': 'average_sold must be less than 100',
            'status_code': 422,
        }

    journey_id = query_params.get('journey')
    if not journey_id:
        return {
            'message': 'journey is required',
            'status_code': 422,
        }

    serializer = JourneySerializer()
    journey = serializer.get_one(journey_id)
    if not journey:
        return {
            'message': 'Journey with id {} does not exist'.format(journey_id),
            'status_code': 404,
        }

    journeySerializer = JourneySerializer()
    buses = journeySerializer.buses_average_sold(
        page=page,
        per_page=per_page,
        average_sold=average_sold,
        journey=journey.instance,
    )

    return {
        'data': {
            'buses': buses,
        },
    }


@csrf_exempt
@api_view(['GET'])
@request
@response
def available_for_sale(payload: dict) -> dict:
    '''
    Obtener las rutas disponibles para la ruta

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
            - journeys: dict
        - message: str
    '''
    query_params = payload.get('query_params')

    page = query_params.get('page', 1)
    per_page = query_params.get('per_page', 10)

    errors = {}

    start = query_params.get('start')
    end = query_params.get('end')
    origen_id = query_params.get('origen_id')
    destination_id = query_params.get('destination_id')

    if not start:
        errors['start'] = 'Start is required'
    if not end:
        errors['end'] = 'End is required'
    if not origen_id:
        errors['origen_id'] = 'Origen is required'
    elif not origen_id.isdigit():
        errors['origen_id'] = 'Origen must be an integer'
    if not destination_id:
        errors['destination_id'] = 'Destination is required'
    elif not destination_id.isdigit():
        errors['destination_id'] = 'Destination must be an integer'

    if errors:
        return {
            'message': errors,
            'status_code': 422,
        }

    start = validate_datetime(start)
    end = validate_datetime(end)
    origen_id = LocationSerializer().get_one(int(origen_id))
    destination_id = LocationSerializer().get_one(int(destination_id))

    if not start:
        errors['start'] = 'Start is not a valid date, must be in format %Y-%m-%d %H:%M'
    if not end:
        errors['end'] = 'End is not a valid date, must be in format %Y-%m-%d %H:%M'
    if not origen_id:
        errors['origen_id'] = 'Origen does not exist'
    if not destination_id:
        errors['destination_id'] = 'Destination does not exist'

    if errors:
        return {
            'message': errors,
            'status_code': 422,
        }

    journeySerializer = JourneySerializer()
    journeys = journeySerializer.available_for_sale(
        page=page,
        per_page=per_page,
        start=start,
        end=end,
        origen=origen_id.instance,
        destination=destination_id.instance,
    )

    return {
        'data': {
            'journeys': journeys,
        },
    }


@csrf_exempt
@api_view(['GET'])
@request
@response
def to_buy(payload: dict) -> dict:
    '''
    Obtener la informacion del viaje para comprar

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
            'status_code': 404,
        }

    ticketSerializer = TicketSerializer()
    tickets = ticketSerializer.to_buy(journey.instance)

    return {
        'data': {
            'journey': journey.data,
            'tickets': tickets.data,
        },
    }
