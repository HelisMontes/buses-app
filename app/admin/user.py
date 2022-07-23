from django.contrib import admin
from app.models.user import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = (
        'identification',
        'name',
        'last_name',
        'email',
        'phone',
        'birth_date',
        'type_user',
        'status',
    )
