from django.urls import path, re_path

from . import views

app_name = 'users'

urlpatterns = [
    path(r'my_info/', views.user_info, name='my_info'),
    path(r'user_info/<str:user_id>/', views.user_info, name='user_info'),
]
