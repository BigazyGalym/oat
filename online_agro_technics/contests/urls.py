from django.urls import path
from . import views

app_name = 'contests'

urlpatterns = [
    path('', views.contest_list, name='contest_list'),
    path('<int:contest_id>/', views.contest_detail, name='contest_detail'),
    path('create/', views.create_contest, name='create_contest'),
]