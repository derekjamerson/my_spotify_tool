from django.urls import path

from . import views

app_name = 'albums'

urlpatterns = [
    path(r'album_info/<str:album_id>/', views.album_info, name='album_info'),
]
