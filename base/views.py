from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from spotify import Spotify
from spotify.oauth import OAuth


def index(request):
    if request.user.is_authenticated:
        return redirect(reverse('libraries:my_library_stats'))
    return render(request, 'index.html')


# noinspection PyUnusedLocal
@require_POST
def spotify_login(request):
    oauth = OAuth()
    auth_url = oauth.create_auth_url()
    return redirect(auth_url)


@require_POST
def spotify_callback(request):
    oauth = OAuth()
    request.session['token_response'] = oauth.get_token_json(request)
    access_token = request.session['token_response']['access_token']
    user = authenticate(access_token=access_token)
    if user is not None:
        login(request, user)
        return redirect(reverse('libraries:my_library_stats'))
    return redirect(reverse('base:index'))


@require_POST
def logout_view(request):
    logout(request)
    return redirect(reverse('base:index'))


@require_POST
def pull_data(request):
    access_token = request.session['token_response']['access_token']
    spotify = Spotify(access_token)
    spotify.pull_library_data(request.user)
    return redirect(reverse('base:index'))
