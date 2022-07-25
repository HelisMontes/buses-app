from django.contrib import admin
from app.models.journey import Journey


@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):
    fields = (
        'origen',
        'destination',
        'bus',
        'user',
        'datetime_start',
        'datetime_end',
        'price',
        'status',
    )
