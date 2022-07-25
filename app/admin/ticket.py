from django.contrib import admin
from app.models.ticket import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'journey',
        'number_seat',
        'datetime_sold',
        'status',
    )
