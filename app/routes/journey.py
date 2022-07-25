from django.urls import path

from app.controllers.journey import get_all
from app.controllers.journey import get_one
from app.controllers.journey import create
from app.controllers.journey import update
from app.controllers.journey import delete
from app.controllers.journey import average_passengers
from app.controllers.journey import buses_average_sold
from app.controllers.journey import available_for_sale


urlpatterns = [
    path('', get_all),
    path('get/<int:pk>', get_one),
    path('create', create),
    path('update', update),
    path('delete', delete),
    path('average_passengers', average_passengers),
    path('buses_average_sold', buses_average_sold),
    path('available-for-sale', available_for_sale),
]
