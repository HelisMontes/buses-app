from django.contrib import admin
from app.models.location import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    fields = (
        'country',
        'city',
        'status',
    )
