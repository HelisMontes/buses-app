from app.decorators.response import response
from app.decorators.methods import clean_get
from app.decorators.methods import clean_post
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from app.serializers.ticket import TicketSerializer


@csrf_exempt
@api_view(['GET'])
@clean_get
@response
def get_all(query_params):
    """Get all tickets"""
    page = query_params.get('page', 1)
    per_page = query_params.get('per_page', 10)

    ticketSerializer = TicketSerializer()
    tickets = ticketSerializer.get_all(
        page=page,
        per_page=per_page,
    )

    return {
        'data': {
            'tickets': tickets.data,
            'meta': {
                'page': page,
                'per_page': per_page,
                'total_items': len(tickets.data),
            },
        },
        'message': 'success',
    }


@csrf_exempt
@api_view(['GET'])
@response
def get_one(request, pk):
    serializer = TicketSerializer()
    ticket = serializer.get_one(pk)
    if not ticket:
        return {
            'message': 'Ticket with id {} does not exist'.format(pk),
            'status': 404,
        }
    return {
        'data': {
            'ticket': ticket.data,
        },
        'message': 'success',
    }


@csrf_exempt
@api_view(['POST'])
@clean_post
@response
def create(body):
    serializer = TicketSerializer(data=body)
    if not serializer.is_valid():
        return {
            'message': serializer.errors,
            'status': 400,
        }

    serializer.save()
    return {
        'data': {
            'ticket': serializer.data,
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

    serializer = TicketSerializer()
    ticket = serializer.get_one(pk)
    if not ticket:
        return {
            'message': 'Ticket with id {} does not exist'.format(pk),
            'status': 404,
        }

    ticket.set_data(body)
    if not ticket.is_valid():
        return {
            'message': ticket.errors,
            'status': 422,
        }

    ticket.save()

    return {
        'data': {
            'ticket': ticket.data,
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

    serializer = TicketSerializer()
    ticket = serializer.get_one(pk)
    if not ticket:
        return {
            'message': 'Ticket with id {} does not exist'.format(pk),
            'status': 404,
        }

    ticket.instance.delete()

    return {
        'message': 'Ticket with id {} has been deleted'.format(pk),
    }
