from django.urls import path
from . import views

app_name = 'helpdesk'

urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),
    path('create/', views.create_ticket, name='create_ticket'),
    path('<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('<int:ticket_id>/close/', views.ticket_close, name='ticket_close'),
    path('api/tickets/create/', views.TicketCreateAPI.as_view(), name='ticket_create_api'),
    path('api/tickets/', views.TicketListAPI.as_view(), name='ticket_list_api'),
    path('user/<int:ticket_id>/', views.user_ticket_detail, name='user_ticket_detail'),
    path('', views.ticket_list, name='ticket_list'),
]