from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class TicketHomeView(TemplateView):
    template_name = 'tickets/home.html'


class PurchaseView(TemplateView):
    template_name = 'tickets/purchase.html'


class TicketDetailPage(TemplateView):
    template_name = 'tickets/detail.html'