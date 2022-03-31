from django.db.models.functions import Lower
from django.shortcuts import render, get_object_or_404

from artists.models import Artist


def all_artists(request):
    artists = Artist.objects.all().order_by(Lower('name'))
    return render(request, 'all_artists.html', {'context': artists})


def single_artist(request, artist_id):
    artist = get_object_or_404(Artist, spotify_id=artist_id)
    tracks = artist.tracks.order_by(Lower('name'))
    return render(request, 'single_artist.html', {'name': artist.name, 'tracks': tracks})
