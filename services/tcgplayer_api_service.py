import os
from typing import Optional

import aiohttp
from datetime import datetime

from aiohttp import ClientSession

TCGPLAYER_CATEGORY_ID = 2
TCGPLAYER_BASE_URL = "https://api.tcgplayer.com"
TCGPLAYER_ACCESS_TOKEN_URL = f'/token'
TCGPLAYER_CATALOG_URL = f'/catalog/categories/{TCGPLAYER_CATEGORY_ID}/'


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
        self.session: Optional[ClientSession] = None

    def init(self, session: ClientSession):
        self.session = session

    def get_authorization_headers(self) -> dict:
        headers = {}
        if self.access_token is not None:
            headers['Authorization'] = f'bearer {self.access_token}'

        return headers

    async def get_card_rarities(self) -> dict:
        return await self._fetch_tcgplayer_resource_with_access_token(
            f'{TCGPLAYER_CATALOG_URL}rarities',
            headers=self.get_authorization_headers()
        )

    async def get_card_printings(self) -> dict:
        return await self._fetch_tcgplayer_resource_with_access_token(
            f'{TCGPLAYER_CATALOG_URL}printings',
            headers=self.get_authorization_headers()
        )

    async def get_card_conditions(self) -> dict:
        return await self._fetch_tcgplayer_resource_with_access_token(
            f'{TCGPLAYER_CATALOG_URL}conditions',
            headers=self.get_authorization_headers()
        )

    async def get_sets(self, offset, limit):
        return await self._fetch_tcgplayer_resource_with_access_token(
            self._get_sets(offset, limit)
        )

    async def _get_sets(self, offset, limit):
        query_params = {
            'offset': offset,
            'limit': limit,
        }
        async with self.session.get(
                f'{TCGPLAYER_CATALOG_URL}groups',
                headers=self.get_authorization_headers(),
                params=query_params
        ) as response:
            return await response.json()

    async def _fetch_tcgplayer_resource_with_access_token(self, url, **kwargs):
        if not await self._check_and_refresh_access_token():
            return None

        print("FETCHING DATA ", url)
        try:
            async with self.session.get(
                    url=url,
                    **kwargs
            ) as response:
                data = await response.json()
                errors = data['errors']
                if errors is None or len(errors) == 0:
                    return data
                else:
                    print(f'ERRORS: {data["errors"]}')
        except aiohttp.ClientConnectionError:
            print('Connection Error')

    async def _check_and_refresh_access_token(self) -> bool:
        if access_token_expired(self.access_token_expiry):
            print("ACCESS TOKEN EXPIRED: Fetching new one")
            client_id = os.environ.get("TCGPLAYER_CLIENT_ID")
            client_secret = os.environ.get("TCGPLAYER_CLIENT_SECRET")

            try:
                async with self.session.post(
                        TCGPLAYER_ACCESS_TOKEN_URL,
                        data={
                            'grant_type': "client_credentials",
                            'client_id': client_id,
                            'client_secret': client_secret,
                        }
                ) as response:
                    data = await response.json()
                    self.access_token = data['access_token']
                    self.access_token_expiry = data['.expires']

                    print("UPDATING ACCESS TOKEN")

                    return True
            except aiohttp.ClientConnectionError:
                print('Connection Error')
                return False
        else:
            return True
