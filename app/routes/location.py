from django.urls import path

from app.controllers.location import get_all
from app.controllers.location import get_one
from app.controllers.location import create
from app.controllers.location import update
from app.controllers.location import delete


urlpatterns = [
    path('', get_all),
    path('get/<int:pk>', get_one),
    path('create', create),
    path('update', update),
    path('delete', delete),
]
