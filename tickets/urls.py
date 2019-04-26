from django.urls import path
from tickets.views import *

urlpatterns = [
    path('', TicketsList.as_view(), name="tickets list"),
    path('add/', NewTicket.as_view(), name="add ticket"),
    path('<int:ticket_id>/', TicketDetails.as_view(), name="ticket details"),
]