from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from tracks.models import Track


@login_required
def track_info(request, track_id):
    track = get_object_or_404(Track, pk=track_id)
    return render(
        request,
        'track_info.html',
        {'track': track},
    )
