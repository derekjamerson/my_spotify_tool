from bs4 import BeautifulSoup
from django.test import TestCase
from django.urls import reverse

from artists.factories import ArtistFactory
from artists.models import Artist
from testing import BaseTestCase


class AllArtistsTestCase(BaseTestCase):
    url = reverse('artists:all_artists')

    def setUp(self):
        super().setUp()
        ArtistFactory.create_batch(3)

    def test_GET_returns_200(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)

    def test_artist_name_sorted(self):
        r = self.client.get(self.url)
        actual_names = self.css_select_get_test(r, 'td.artist-name')
        expected_names = list(Artist.objects.values_list('name', flat=True).order_by('name'))
        self.assertEqual(actual_names, expected_names)

    def test_link_to_drill_down(self):
        r = self.client.get(self.url)
        actual_urls = self.css_select_get_attributes(r, 'td.artist-name a', ['href'])
        expected_urls = [
            {'href': reverse('artists:single_artist', kwargs=dict(artist_id=artist.pk))}
            for artist in Artist.objects.all()
        ]
        self.assertCountEqual(actual_urls, expected_urls)
