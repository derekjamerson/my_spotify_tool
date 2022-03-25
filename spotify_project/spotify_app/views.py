from django.shortcuts import render, redirect
from spotify_api.spotify_auth import SpotifyAuth


def spotify_login_redirect(request):
    return redirect(create_auth_url())