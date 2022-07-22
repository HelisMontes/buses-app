from django.http import JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view


@csrf_exempt
@api_view(['GET'])
def get(request):
    return JsonResponse({}, status=201)


urlpatterns = [
    path('', get),
]
