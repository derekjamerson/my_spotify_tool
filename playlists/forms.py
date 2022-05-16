from datetime import datetime

from django import forms
from django.db.models.functions import Lower

from artists.models import Artist
from playlists.utils import PlaylistUtils
from spotify.base import Spotify


class MakePlaylistForm(forms.Form):
    name = forms.CharField()
    artists = forms.ModelMultipleChoiceField(Artist.objects.none())

    # TODO get artists by user
    def __init__(self, *args, user, token=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.token = token
        self.fields['artists'].queryset = Artist.objects.all().order_by(Lower('name'))

    def save(self):
        utils = PlaylistUtils()
        playlist = utils.create_by_artists(
            user=self.user,
            name=self.cleaned_data['name'],
            artists=self.cleaned_data['artists'],
        )
        spotify = Spotify(self.token)
        spotify.create_playlist(self.user, playlist)
        spotify.add_tracks_to_playlist(self.user, playlist)

    def clean_artists(self):
        if len(self.cleaned_data['artists']) > 5:
            raise forms.ValidationError('Max artists is 5.')
        return self.cleaned_data['artists']
