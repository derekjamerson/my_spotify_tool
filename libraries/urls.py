from django.urls import path, re_path

from . import views

app_name = 'libraries'

urlpatterns = [
    path(r'library_stats/<str:user_id>/', views.library_stats, name='library_stats'),
    path(
        r'library_stats/',
        views.library_stats,
        name='my_library_stats',
        kwargs={'user_id': None},
    ),
    path(
        r'compare_stats/',
        views.compare_stats,
        name='compare_stats',
    ),
]
