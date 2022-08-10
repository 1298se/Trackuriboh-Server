import os
import requests
from datetime import datetime

TCGPLAYER_ACCESS_TOKEN_URL = "https://api.tcgplayer.com/token"


def access_token_expired(expiry) -> bool:
    if expiry is None:
        return True
    # Sat, 20 Aug 2022 18:39:21 GMT
    expiry_date = datetime.strptime(expiry, "%a, %d %b %Y %H:%M:%S %Z")

    return datetime.now() > expiry_date


class TCGPlayerRequestHandler:
    def __init__(self):
        self.access_token = None
        self.access_token_expiry = None

    def fetchTCGPlayerResourceWithAccessToken(self, request_func):
        if access_token_expired(self.access_token_expiry):
            print("ACCESS TOKEN EXPIRED: Fetching new one")
            client_id = os.environ.get("TCGPLAYER_CLIENT_ID")
            client_secret = os.environ.get("TCGPLAYER_CLIENT_SECRET")

            request = requests.post(url=TCGPLAYER_ACCESS_TOKEN_URL, data={
                'grant_type': "client_credentials",
                'client_id': client_id,
                'client_secret': client_secret,
            })

            response = request.json()

            self.access_token = response['access_token']
            self.access_token_expiry = response['.expires']

        request_func()
