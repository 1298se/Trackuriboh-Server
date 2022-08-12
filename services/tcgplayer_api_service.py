import os
import requests
from datetime import datetime

TCGPLAYER_CATEGORY_ID = 2
TCGPLAYER_BASE_URL = "https://api.tcgplayer.com/"
TCGPLAYER_ACCESS_TOKEN_URL = f'{TCGPLAYER_BASE_URL}token'
TCGPLAYER_CATALOG_URL = f'{TCGPLAYER_BASE_URL}catalog/categories/{TCGPLAYER_CATEGORY_ID}/'


def access_token_expired(expiry) -> bool:
    if expiry is None:
        return True
    # Sat, 20 Aug 2022 18:39:21 GMT
    expiry_date = datetime.strptime(expiry, "%a, %d %b %Y %H:%M:%S %Z")

    return datetime.now() > expiry_date


class TCGPlayerApiService:
    def __init__(self):
        self.access_token = None
        self.access_token_expiry = None

    def get_authorization_headers(self) -> dict:
        headers = {}
        if self.access_token is not None:
            headers['Authorization'] = f'bearer {self.access_token}'

        return headers

    def get_card_rarities(self) -> dict:
        return self._fetchTCGPlayerResourceWithAccessToken(
            lambda: requests.get(f'{TCGPLAYER_CATALOG_URL}rarities', headers=self.get_authorization_headers()).json()
        )

    def get_card_printings(self) -> dict:
        return self._fetchTCGPlayerResourceWithAccessToken(
            lambda: requests.get(f'{TCGPLAYER_CATALOG_URL}printings', headers=self.get_authorization_headers()).json()
        )

    def get_card_conditions(self) -> dict:
        return self._fetchTCGPlayerResourceWithAccessToken(
            lambda: requests.get(f'{TCGPLAYER_CATALOG_URL}conditions', headers=self.get_authorization_headers()).json()
        )

    def _fetchTCGPlayerResourceWithAccessToken(self, request_func) -> dict:
        if access_token_expired(self.access_token_expiry):
            print("ACCESS TOKEN EXPIRED: Fetching new one")
            client_id = os.environ.get("TCGPLAYER_CLIENT_ID")
            client_secret = os.environ.get("TCGPLAYER_CLIENT_SECRET")

            try:
                response = requests.post(url=TCGPLAYER_ACCESS_TOKEN_URL, data={
                    'grant_type': "client_credentials",
                    'client_id': client_id,
                    'client_secret': client_secret,
                }).json()

                self.access_token = response['access_token']
                self.access_token_expiry = response['.expires']
            except ConnectionError:
                pass
        try:
            result = request_func()

            errors = result['errors']
            if errors is None or len(errors) == 0:
                return result
            else:
                print(f'ERRORS: {result["errors"]}')
                raise ConnectionError
        except ConnectionError:
            pass
