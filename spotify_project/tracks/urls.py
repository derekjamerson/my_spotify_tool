from django.urls import path, re_path

from . import views

app_name = 'tracks'

urlpatterns = [
    path(r'track_info/<str:track_id>/', views.track_info, name='track_info'),
]
