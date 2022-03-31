import time

from django.db.models.functions import Lower

from albums.models import Album
from artists.models import Artist
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from spotify import Spotify
from spotify.oauth import OAuth
from tracks.models import Track


def spotify_login(request):
    oauth = OAuth()
    auth_url = oauth.create_auth_url()
    return redirect(auth_url)


def spotify_callback(request):
    oauth = OAuth()
    request.session['token_response'] = oauth.get_token_json(request)
    return redirect(reverse('base:pull_data'))


def pull_data(request):
    start_time = time.time()
    access_token = request.session['token_response']['access_token']
    spotify = Spotify(access_token)
    spotify.pull_library_data()
    return HttpResponse(
        f'time: {time.time() - start_time} | '
        f'tracks: {Track.objects.count()}, '
        f'artists: {Artist.objects.count()}, '
        f'albums: {Album.objects.count()} | '
    )



