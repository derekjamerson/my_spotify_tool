from django.urls import re_path, path

from . import views

app_name = 'artists'

urlpatterns = [
    re_path(r'^all_artists/$', views.all_artists, name='all_artists'),
    path(r'single_artist/<str:artist_id>/', views.single_artist, name='single_artist'),
]
