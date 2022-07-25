from django.contrib import admin
from app.models.bus import Bus


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    fields = (
        'brand',
        'model',
        'color',
        'plate',
        'quantity_seats',
        'image',
        'year',
        'status',
    )
