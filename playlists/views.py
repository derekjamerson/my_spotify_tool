from datetime import datetime

from django.shortcuts import redirect, render
from django.urls import reverse

from playlists.forms import MakePlaylistForm


def create_playlist(request):
    form = MakePlaylistForm(user=request.user)
    if request.method == 'POST':
        form = MakePlaylistForm(
            request.POST,
            user=request.user,
            token=request.session['token_response']['access_token'],
        )
        if form.is_valid():
            form.save()
            return redirect(reverse('base:index'))
    context = {
        'form': form,
    }
    return render(request, 'create_playlist.html', context)
