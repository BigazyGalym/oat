from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.forum_list, name='forum_list'),
    path('post/<int:post_id>/', views.forum_post_detail, name='post_detail'),
    path('create/', views.create_forum_post, name='create_post'),
]