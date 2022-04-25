from django.urls import path, re_path

from . import views

app_name = 'artists'

urlpatterns = [
    re_path(
        r'^my_artists/$', views.all_artists, name='my_artists', kwargs={'mine': True}
    ),
    re_path(r'^all_artists/$', views.all_artists, name='all_artists'),
    path(r'user_artists/<str:user_id>/', views.all_artists, name='user_artists'),
    path(r'single_artist/<str:artist_id>/', views.single_artist, name='single_artist'),
]
