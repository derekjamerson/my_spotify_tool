from artists.models import Artist
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, render


def all_artists(request):
    artists = request.user.library.artists.all().order_by(Lower('name'))
    return render(request, 'all_artists.html', {'artists': artists})


def single_artist(request, artist_id):
    artist = get_object_or_404(Artist, spotify_id=artist_id)
    tracks = request.user.library.tracks.filter(artists=artist).order_by(Lower('name'))
    return render(
        request, 'single_artist.html', {'name': artist.name, 'tracks': tracks}
    )
