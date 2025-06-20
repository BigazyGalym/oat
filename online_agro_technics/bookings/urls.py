from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('worker/availability/', views.worker_availability, name='worker_availability'),
    path('create/<int:availability_id>/', views.create_booking, name='create_booking'),
    path('workers/', views.available_workers, name='available_workers'),
    path('customer/bookings/', views.customer_bookings, name='customer_bookings'),
    path('worker/bookings/', views.worker_bookings, name='worker_bookings'),
    path('confirm/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]