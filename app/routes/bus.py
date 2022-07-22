from django.urls import path

from app.controllers.bus_controller import get_one
from app.controllers.bus_controller import create
from app.controllers.bus_controller import update


urlpatterns = [
    path('get-one/<int:pk>', get_one),
    path('create', create),
    path('update', update),
    # path('get-all', get),
]
