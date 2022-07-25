from django.urls import path

from app.controllers.user import get_all
from app.controllers.user import get_one
from app.controllers.user import create
from app.controllers.user import update
from app.controllers.user import delete


urlpatterns = [
    path('', get_all),
    path('get/<int:pk>', get_one),
    path('create', create),
    path('update', update),
    path('delete', delete),
]
