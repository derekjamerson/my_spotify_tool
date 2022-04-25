import json
from unittest.mock import Mock, patch

import requests
from spotify.oauth import OAuth
from testing import BaseTestCase
from testing.base import MockResponse


class OAuthTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = 'https://accounts.spotify.com/api/token'
        self.oauth = OAuth()

    def test_get_token_json(self):
        expected = {'item': 'dummy_data'}

        def mock_json(*args, **kwargs):
            return expected

        request_object = MockResponse(GET={'code': 'dummy_code'})
        with patch('requests.post', return_value=Mock(json=mock_json)):
            r = self.oauth.get_token_json(request_object)
        self.assertEqual(r, expected)
