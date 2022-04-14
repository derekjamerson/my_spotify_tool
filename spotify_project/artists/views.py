from artists.models import Artist
from django.contrib.auth import get_user_model
from django.db.models.functions import Lower
from django.http import Http404
from django.shortcuts import get_object_or_404, render


def get_source_all_artists(*, user, user_id, mine):
    if user_id:
        user = get_object_or_404(get_user_model(), pk=user_id)
        return user.library.artists.all()
    if user.is_authenticated:
        if mine:
            return user.library.artists.all()
        return Artist.objects.all()
    if mine:
        raise Http404()
    return Artist.objects.all()


def all_artists(request, user_id=None, mine=False):
    source = get_source_all_artists(user=request.user, user_id=user_id, mine=mine)
    artists = source.order_by(Lower('name'))
    return render(request, 'all_artists.html', {'artists': artists})


def single_artist(request, artist_id):
    artist = get_object_or_404(Artist, spotify_id=artist_id)
    tracks = request.user.library.tracks.filter(artists=artist).order_by(Lower('name'))
    return render(
        request, 'single_artist.html', {'name': artist.name, 'tracks': tracks}
    )
