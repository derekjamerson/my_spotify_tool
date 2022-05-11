from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from albums.models import Album


@login_required
def album_info(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    return render(
        request,
        'album_info.html',
        {'album': album},
    )
