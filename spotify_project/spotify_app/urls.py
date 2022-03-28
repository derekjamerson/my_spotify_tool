from django.urls import re_path

from . import views

app_name = 'spotify_app'

urlpatterns = [
    re_path(r'^spotify_login/$', views.spotify_login, name='spotify_login'),
    re_path(r'^callback/$', views.spotify_callback, name='spotify_callback'),
]
