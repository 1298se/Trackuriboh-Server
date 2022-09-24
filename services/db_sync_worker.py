import asyncio
from datetime import datetime
from typing import Optional

from flask.ctx import AppContext

from repositories.tcgplayer_catalog_repository import TCGPlayerCatalogRepository
from services import paginate


class DatabaseSyncWorker:
    def __init__(self):
        self.app_context = None
        self.catalog_repository: Optional[TCGPlayerCatalogRepository] = None

    def init(self, catalog_repository: TCGPlayerCatalogRepository, app_context: AppContext):
        self.catalog_repository = catalog_repository
        self.app_context = app_context

    def _add_updated_set_models(self, outdated_sets: list, set_responses: list[dict]):
        from models.set import Set

        with self.app_context:
            for set_response in set_responses:
                response_set_model = Set.from_tcgplayer_response(set_response)
                existing_set_model: Set = Set.query.get(response_set_model.id)

                if (existing_set_model is None or
                        existing_set_model.modified_date < response_set_model.modified_date):
                    outdated_sets.append(response_set_model)

    def _convert_and_insert_cards_and_skus(self, card_responses):
        from models.card import Card
        from models.sku import Sku

        self.catalog_repository.insert_cards(
            map(lambda card_response: Card.from_tcgplayer_response(card_response), card_responses)
        )

        for card_response in card_responses:
            self.catalog_repository.insert_skus(
                map(lambda sku_response: Sku.from_tcgplayer_response(sku_response), card_response['skus'])
            )

    async def _fetch_cards_in_set(self, set_id: int) -> list[dict]:
        print(set_id)
        set_card_count = await self.catalog_repository.fetch_total_card_count(set_id)
        set_cards = []

        await paginate(
            total=set_card_count,
            async_paginate_fn=lambda offset, limit: self.catalog_repository.fetch_cards(offset, limit, set_id),
            on_paginated=lambda card_responses: set_cards.extend(card_responses)
        )

        return set_cards

    async def update_card_database(self):
        from models.condition import Condition
        from models.printing import Printing

        print(f'{self.__class__.__name__} started at {datetime.now()}')

        printing_responses, condition_responses = await asyncio.gather(*[
            self.catalog_repository.fetch_card_printings(),
            self.catalog_repository.fetch_card_conditions(),
        ])

        condition_models = list(map(lambda x: Condition.from_tcgplayer_response(x), condition_responses))
        printing_models = list(map(lambda x: Printing.from_tcgplayer_response(x), printing_responses))

        self.catalog_repository.insert_conditions(condition_models)
        self.catalog_repository.insert_printings(printing_models)

        set_total_count = await self.catalog_repository.fetch_total_card_set_count()

        outdated_sets = []
        await paginate(
            total=set_total_count,
            async_paginate_fn=self.catalog_repository.fetch_card_sets,
            on_paginated=lambda set_responses: self._add_updated_set_models(outdated_sets, set_responses)
        )

        print(f'{len(outdated_sets)} sets are oudated: {[outdated_set.name for outdated_set in outdated_sets]}')

        self.catalog_repository.insert_sets(outdated_sets)

        # We want to "paginate" on all the card sets and fetch the cards in each set. Hence, we call paginate
        # with pagination_size=1.
        await paginate(
            total=len(outdated_sets),
            async_paginate_fn=lambda offset, limit: self._fetch_cards_in_set(outdated_sets[offset].id),
            on_paginated=lambda card_responses: self._convert_and_insert_cards_and_skus(card_responses),
            num_parallel_requests=1,
            pagination_size=1,
        )

        print(f'{self.__class__.__name__} done at {datetime.now()}')
