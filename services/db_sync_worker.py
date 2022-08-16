import asyncio
from typing import Any

from aiohttp import ClientSession

from repositories.tcgplayer_catalog_repository import TCGPlayerCatalogRepository

MAX_PARALLEL_REQUESTS = 10
PAGINATION_SIZE = 100


class DatabaseSyncWorker:
    def __init__(self):
        self.catalog_repository = None

    def init(self, catalog_repository: TCGPlayerCatalogRepository):
        self.catalog_repository = catalog_repository

    async def update_card_database(self):
        from models.condition import Condition
        from models.rarity import Rarity
        from models.printing import Printing

        print("RUNNING")

        catalog_data = await asyncio.gather(*[
            self.catalog_repository.fetch_card_rarities(),
            self.catalog_repository.fetch_card_printings(),
            self.catalog_repository.fetch_card_conditions(),
        ])

        print(catalog_data)



    def _paginate(self, total, offset, limit, paginate_fn, on_paginated):
        batch_increments = min(total, MAX_PARALLEL_REQUESTS * PAGINATION_SIZE)

        for batch_offset in range(0, total, batch_increments):
            pass
