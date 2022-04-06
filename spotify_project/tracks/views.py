from django.shortcuts import get_object_or_404, render
from tracks.models import Track


def track_info(request, track_id):
    track = get_object_or_404(Track, pk=track_id)
    artists = list(track.artists.all())
    seconds = (int(track.duration_ms) / 1000) % 60
    minutes = (int(track.duration_ms) / (1000 * 60)) % 60
    properties = {
        'spotify_id': track.spotify_id,
        'album': track.album,
        'duration': f'{int(minutes)}:{round(seconds)}',
        'is_explicit': track.is_explicit,
        'popularity': track.popularity,
    }
    return render(
        request,
        'track_info.html',
        {'properties': properties, 'name': track.name, 'artists': artists},
    )
