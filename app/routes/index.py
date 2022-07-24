from django.urls import path
from django.urls import include


urlpatterns = [
    path(
        'bus/',
        include('app.routes.bus'),
    ),
    path(
        'location/',
        include('app.routes.location'),
    ),
    path(
        'user/',
        include('app.routes.user'),
    ),
]
