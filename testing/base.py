import json
from contextlib import contextmanager

from bs4 import BeautifulSoup
from django.test import TestCase

from albums.factories import AlbumFactory
from artists.factories import ArtistFactory
from tracks.factories import TrackFactory


class BaseTestCase(TestCase):
    @staticmethod
    def css_select_get_text(response, css_selector):
        soup = BeautifulSoup(response.content, features='html.parser')
        text_groups = []
        for element in soup.select(css_selector):
            text_groups.append(element.text.strip())
        return text_groups

    @staticmethod
    def css_select_get_attributes(response, css_selector, attributes):
        soup = BeautifulSoup(response.content, features='html.parser')
        result = []
        for element in soup.select(css_selector):
            attr_dict = {}
            for attribute in attributes:
                attr_dict[attribute] = element.attrs.get(attribute, None)
            result.append(attr_dict)
        return result

    @contextmanager
    def assert_num_objects_created(self, counts):
        before_counts = {}
        after_counts = {}
        for Model in counts:
            before_counts[Model] = Model.objects.count()
        yield
        for Model in counts:
            after_counts[Model] = Model.objects.count()
        for Model in counts:
            delta = after_counts[Model] - before_counts[Model]
            self.assertEqual(delta, counts[Model], Model)

    @property
    def dummy_library_data(self):
        with open('track_response_example.json') as json_file:
            dummy_data = json.load(json_file)
        for track in dummy_data['items']:
            yield track['track']

    def add_dummy_objects_to_db(self, add_tracks=True):
        artists_to_be_added = []
        albums_to_be_added = []
        tracks_to_be_added = []
        for track in self.dummy_library_data:
            for artist in track['artists']:
                new_artist = ArtistFactory.build(pk=artist['id'], name=artist['name'])
                artists_to_be_added.append(new_artist)
            new_album = AlbumFactory.build(
                pk=track['album']['id'], name=track['album']['name']
            )
            albums_to_be_added.append(new_album)
            new_track = TrackFactory.build(
                pk=track['id'], name=track['name'], album=new_album
            )
            tracks_to_be_added.append(new_track)
        for artist in set(artists_to_be_added):
            artist.save()
        for album in set(albums_to_be_added):
            album.save()
        if add_tracks:
            for track in set(tracks_to_be_added):
                track.save()


class MockResponse:
    def __init__(self, GET=None):
        if not GET:
            GET = {}
        self.GET = GET
