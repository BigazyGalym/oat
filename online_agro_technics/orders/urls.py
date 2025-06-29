from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('worker/orders/', views.worker_orders, name='worker_orders'),
    path('worker/dashboard/', views.worker_dashboard, name='worker_dashboard'),
    path('accept/<int:order_id>/', views.accept_order, name='accept_order'),
    path('start/<int:order_id>/', views.start_order, name='start_order'),
    path('complete/<int:order_id>/', views.complete_order, name='complete_order'),
    path('create/', views.create_order, name='create_order'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('cancel_customer/<int:order_id>/', views.cancel_customer_order, name='cancel_customer_order'),
    path('rate/<int:order_id>/', views.rate_order, name='rate_order'),
    path('my-orders/', views.my_orders_view, name='my_orders'),
    
]