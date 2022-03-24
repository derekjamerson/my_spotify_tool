from spotify_api.spotify_api import SpotifyApi

from spotify_api.spotify_auth import SpotifyAuth


if __name__ == '__main__':
    auth = SpotifyAuth('user-read-private')
    token = auth.get_access_token()
    api_access = SpotifyApi()
    print(api_access.get_user_profile(token))
