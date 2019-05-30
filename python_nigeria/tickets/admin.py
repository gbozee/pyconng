from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.
from .models import (
    Ticket, TicketPrice, Coupon, TicketSale
)

class TicketSaleResource(resources.ModelResource):
    ticket_type = resources.Field()
    email = resources.Field()
    class Meta:
        model = TicketSale
        fields = ('the_ticket_id', 'full_name', 'diet', 'tagline', 'ticket')

    def dehydrate_ticket_type(self, obj):
        return obj.ticket.ticket_type

    def dehydrate_email(self, obj):
        return obj.user.email

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'order', 'ticket_type', 'amount', 'status', 'multiple_tickets', 'quantity']
    list_filter = ['ticket_type__name', 'status']
    search_fields = ['user__email', 'user__username']


@admin.register(TicketPrice)
class TicketPriceAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'current_price', 'early_price_count', 'regular_count', 'total', 'remaining']

    def total(self, obj):
        return obj.purchased_count

    def remaining(self, obj):
        return obj.early_price_count + obj.regular_count - obj.purchased_count

    def get_queryset(self, request):
        query = super(TicketPriceAdmin, self).get_queryset(request)

        return query.with_tickets_purchased()


@admin.register(Coupon)
class CouponAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['value', 'expired', 'number_of_usage', 'counts']
    actions = 'mark_as_expired'

    def counts(self, obj):
        return obj.usages.count()

    def mark_as_expired(self, request, queryset):
        queryset.update(expired=True)


@admin.register(TicketSale)
class TicketSaleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = TicketSaleResource
    list_display = ['the_ticket_id', 'full_name', 'ticket_type', 'diet', 'tagline', 'ticket']
    list_filter = ['ticket__ticket_type']
    search_fields = ['user__email','full_name','user__username',]

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('pk')

    def ticket_type(self, obj):
        return obj.ticket.ticket_type
