from django.urls import path
from tickets import views

urlpatterns = [
    path('', views.TicketsList.as_view(), name="tickets list"),
    path('add/', views.NewTicket.as_view(), name="add ticket"),
    path('<int:ticket_id>/', views.TicketDetails.as_view(), name="ticket details"),
]