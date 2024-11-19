from django.urls import path
from . import views

urlpatterns = [
    path("", views.ticket_list, name="ticket_list"),
    path("get_tickets", views.get_tickets, name="get_tickets"),
    path("tickets/<int:ticket_id>/", views.ticket_detail, name="ticket_detail"),
    path("tickets/new/", views.submit_ticket, name="submit_ticket"),
]
