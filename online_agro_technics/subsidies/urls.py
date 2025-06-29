from django.urls import path
from . import views

app_name = 'subsidies'

urlpatterns = [
    path('', views.subsidies_info, name='subsidies_info'),
    path('inquiry/', views.submit_inquiry, name='submit_inquiry'),
]