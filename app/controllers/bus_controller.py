from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from app.serializers.bus import BusSerializer


@csrf_exempt
@api_view(['GET'])
def get_one(request, pk):
    serializer = BusSerializer()
    bus = serializer.get_one(pk)
    if not bus:
        return JsonResponse({
            'error': 'Bus with id {} does not exist'.format(pk)
        }, status=404)
    return JsonResponse(bus.data, status=200)


@csrf_exempt
@api_view(['POST'])
def create(request):
    data = JSONParser().parse(request)
    serializer = BusSerializer(data=data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)

    serializer.save()
    return JsonResponse(serializer.data, status=201)


@csrf_exempt
@api_view(['POST'])
def update(request):
    data = JSONParser().parse(request)

    if not data.get('id'):
        return JsonResponse({'error': 'id is required'}, status=400)

    pk = data.get('id')

    serializer = BusSerializer()
    bus = serializer.get_one(pk)
    if not bus:
        return JsonResponse({
            'error': 'Bus with id {} does not exist'.format(pk)
        }, status=404)

    bus.initial_data = data
    if not bus.is_valid():
        return JsonResponse(bus.errors, status=422)

    bus.save()

    return JsonResponse(bus.data, status=201)
