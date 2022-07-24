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
    path(
        'journey/',
        include('app.routes.journey'),
    ),
    path(
        'ticket/',
        include('app.routes.ticket'),
    ),
]
