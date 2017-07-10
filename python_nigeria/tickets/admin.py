from django.contrib import admin

# Register your models here.
from .models import Ticket, TicketPrice, Coupon


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'order', 'ticket_type', 'amount','status', 'multiple_tickets', 'quantity']
    list_filter = ['ticket_type__name', 'status']


@admin.register(TicketPrice)
class TicketPriceAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['value', 'expired']
    actions = 'mark_as_expired'

    def mark_as_expired(self, request, queryset):
        queryset.update(expired=True)
