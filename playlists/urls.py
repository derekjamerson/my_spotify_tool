from django.urls import path

from playlists import views

app_name = 'playlists'

urlpatterns = [
    path(r'create/', views.create_playlist, name='create'),
]
