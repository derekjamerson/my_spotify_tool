import json
from unittest.mock import Mock, patch

import requests
from spotify.oauth import OAuth
from testing import BaseTestCase


class OAuthTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = 'https://accounts.spotify.com/api/token'
        self.oauth = OAuth()

    @patch.object(requests, 'post')
    def test_get_token_json(self, mock_request):
        expected = {'item': 'dummy_data'}
        request_object = requests.Response()
        request_object.status_code = 200
        request_object.json = json.loads(json.dumps({'code': 'dummy_code'}))
        mock_request.return_value = request_object
        with patch(
            'requests.post', return_value=Mock(status_code=200, json=lambda: expected)
        ):
            r = self.oauth.get_token_json(mock_request)
        self.assertEqual(r, expected)
