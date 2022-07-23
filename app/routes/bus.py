from django.urls import path

from app.controllers.bus import get_all
from app.controllers.bus import get_one
from app.controllers.bus import create
from app.controllers.bus import update
from app.controllers.bus import delete


urlpatterns = [
    path('', get_all),
    path('get/<int:pk>', get_one),
    path('create', create),
    path('update', update),
    path('delete', delete),
]
