from django.urls import path

from app.controllers.ticket import get_all
from app.controllers.ticket import get_one
from app.controllers.ticket import create
from app.controllers.ticket import update
from app.controllers.ticket import delete


urlpatterns = [
    path('', get_all),
    path('get/<int:pk>', get_one),
    path('create', create),
    path('update', update),
    path('delete', delete),
]
