from django.urls import path

from . import views

app_name = 'base'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'spotify_login/', views.spotify_login, name='login'),
    path(r'callback/', views.spotify_callback, name='callback'),
    path(r'pull_data/', views.pull_data, name='pull_data'),
    path(r'logout/', views.logout_view, name='logout'),
]
