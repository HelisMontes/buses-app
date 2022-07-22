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
    if not bus.get('is_valid'):
        return JsonResponse(bus, status=404)
    return JsonResponse(bus['data'].data, status=200)


@csrf_exempt
@api_view(['POST'])
def create(request):
    data = JSONParser().parse(request)
    serializer = BusSerializer(data=data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)

    serializer.save()
    return JsonResponse(serializer.data, status=201)
