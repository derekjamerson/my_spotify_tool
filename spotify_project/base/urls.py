from django.urls import re_path

from . import views

app_name = 'base'

urlpatterns = [
    re_path(r'^spotify_login/$', views.spotify_login, name='login'),
    re_path(r'^callback/$', views.spotify_callback, name='callback'),
    re_path(r'^pull_data/$', views.pull_data, name='pull_data'),
    re_path(r'^all_artists/$', views.all_artists, name='all_artists'),
    re_path(r'^single_artist/(?P<artist_id>[^/]+)/(?P<name>[^/]+)/$', views.single_artist, name='single_artist'),
]
