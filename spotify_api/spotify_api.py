import requests


class SpotifyApi(object):
    base_url = 'https://api.spotify.com/v1'

    def get_user_profile(self, access_token):
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        user_profile = requests.get(self.base_url + '/me', headers=headers)
        return user_profile.json()
