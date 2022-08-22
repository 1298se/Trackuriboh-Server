import os
from asyncio import Lock
from typing import Optional

import aiohttp
from datetime import datetime

from aiohttp import ClientSession

TCGPLAYER_CATEGORY_ID = 2
TCGPLAYER_BASE_URL = "https://api.tcgplayer.com"
TCGPLAYER_ACCESS_TOKEN_URL = f'/token'
TCGPLAYER_PRICING_URL = '/pricing/sku/'
TCGPLAYER_CATALOG_URL = '/catalog/'
TCGPLAYER_CATALOG_CATEGORIES_URL = f'{TCGPLAYER_CATALOG_URL}categories/{TCGPLAYER_CATEGORY_ID}/'


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
        self.lock = Lock()

    def init(self, session: ClientSession):
        self.session = session

    async def get_authorization_headers(self) -> dict:
        async with self.lock:
            headers = {}

            if await self._check_and_refresh_access_token():
                headers['Authorization'] = f'bearer {self.access_token}'

            return headers

    async def get_card_printings(self) -> dict:
        return await self._fetch_tcgplayer_resource(
            f'{TCGPLAYER_CATALOG_CATEGORIES_URL}printings',
            headers=await self.get_authorization_headers()
        )

    async def get_card_conditions(self) -> dict:
        return await self._fetch_tcgplayer_resource(
            f'{TCGPLAYER_CATALOG_CATEGORIES_URL}conditions',
            headers=await self.get_authorization_headers()
        )

    async def get_sets(self, offset, limit):
        query_params = {
            'offset': offset,
            'limit': limit,
        }

        return await self._fetch_tcgplayer_resource(
            f'{TCGPLAYER_CATALOG_CATEGORIES_URL}groups',
            headers=await self.get_authorization_headers(),
            params=query_params,
        )

    async def get_cards(self, offset, limit, set_id=None):
        query_params = {
            'getExtendedFields': "true",
            'includeSkus': "true",
            'productTypes': ["Cards"],
            'offset': offset,
            'limit': limit,
            'categoryId': TCGPLAYER_CATEGORY_ID,
        }

        if set_id is not None:
            query_params['groupId'] = set_id

        return await self._fetch_tcgplayer_resource(
            f'{TCGPLAYER_CATALOG_URL}products',
            headers=await self.get_authorization_headers(),
            params=query_params
        )

    async def get_sku_prices(self, sku_ids: list[int]):
        return await self._fetch_tcgplayer_resource(
            f'{TCGPLAYER_PRICING_URL}{",".join([str(sku_id) for sku_id in sku_ids])}',
            headers=await self.get_authorization_headers(),
        )

    async def _fetch_tcgplayer_resource(self, url, **kwargs):
        try:
            async with self.session.get(
                    url=url,
                    **kwargs
            ) as response:
                data = await response.json()
                errors = data.get('errors')
                if errors is None or len(errors) == 0 or errors[0] == "No products were found.":
                    print(f'SUCCESS on request {url}, {kwargs}')
                    return data
                else:
                    print(f'ERRORS: {data["errors"]} on request {url}, {kwargs}')
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
