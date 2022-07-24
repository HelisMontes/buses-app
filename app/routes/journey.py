from django.urls import path

from app.controllers.journey import get_all
from app.controllers.journey import get_one
from app.controllers.journey import create
from app.controllers.journey import update
from app.controllers.journey import delete


urlpatterns = [
    path('', get_all),
    path('get/<int:pk>', get_one),
    path('create', create),
    path('update', update),
    path('delete', delete),
]
