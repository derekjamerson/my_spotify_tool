import base64
import os
import urllib
from urllib.parse import urlencode
from django.http import HttpResponse, JsonResponse

import requests
from django.shortcuts import redirect
# from spotify_project.spotify_project.settings import REDIRECT_URI, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from django.urls import reverse

from spotify import Spotify

from tracks.models import Track


def spotify_login(request):
    auth_endpoint = 'https://accounts.spotify.com/authorize'
    scope = [
        'user-read-private',
        'user-read-email',
        'user-library-read',
    ]
    payload = {
        'client_id': os.getenv('SPOTIFY_CLIENT_ID'),
        'redirect_uri': os.getenv('REDIRECT_URI'),
        'scope': ' '.join(scope),
        'response_type': 'code',
    }
    auth_url = auth_endpoint + '?' + urllib.parse.urlencode(payload)
    return redirect(auth_url)


def spotify_callback(request):
    token_uri = 'https://accounts.spotify.com/api/token'
    auth_string = os.getenv('SPOTIFY_CLIENT_ID') + ':' + os.getenv('SPOTIFY_CLIENT_SECRET')
    auth_head = base64.b64encode(auth_string.encode('ascii')).decode('ascii')
    headers = {
        'Authorization': 'Basic ' + auth_head,
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    body = {
        'code': request.GET['code'],
        'redirect_uri': os.getenv('REDIRECT_URI'),
        'grant_type': 'authorization_code',
    }
    response = requests.post(token_uri, data=urlencode(body), headers=headers, json=True)
    request.session['token_response'] = response.json()
    return redirect(reverse('base:pull_data'))


# possibly need to pull into utils. doing a lot
# need collision checking
# can return count of objects for verify
def pull_data(request):
    token = request.session['token_response']['access_token']
    spotify = Spotify(token)
    for track in spotify.tracks:
        Track.objects.create(pk=track['id'], name=track['name'])
    return HttpResponse(f'{Track.objects.count()}')
