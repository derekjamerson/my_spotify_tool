import time

from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.urls import reverse

from spotify import Spotify
from spotify.oauth import OAuth


def index(request):
    return render(request, 'index.html')


def spotify_login(request):
    oauth = OAuth()
    auth_url = oauth.create_auth_url()
    return redirect(auth_url)


def spotify_callback(request):
    oauth = OAuth()
    request.session['token_response'] = oauth.get_token_json(request)
    access_token = request.session['token_response']['access_token']
    spotify = Spotify(access_token)
    user = spotify.fetch_current_user()
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    if user is not None:
        login(request, user)
    return redirect(reverse('base:pull_data'))


def logout_view(request):
    logout(request)
    return redirect(reverse('base:index'))


def pull_data(request):
    start_time = time.time()
    access_token = request.session['token_response']['access_token']
    spotify = Spotify(access_token)
    spotify.pull_library_data()
    print(f'time: {time.time() - start_time}')
    return redirect(reverse('base:index'))
