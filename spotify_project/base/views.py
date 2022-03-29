from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from artists.models import Artist
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
    access_token = request.session['token_response']['access_token']
    spotify = Spotify(access_token)
    created_rows = spotify.pull_library_data()
    return HttpResponse(f'tracks: {Track.objects.count()} artists: {Artist.objects.count()} created: {created_rows}')
