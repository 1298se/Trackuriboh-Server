from repositories.catalog_repository import CatalogRepository


class DatabaseSyncWorker:
    def __init__(self, catalog_repository: CatalogRepository):
        self.catalog_repository = catalog_repository

    def update_card_database(self):
        from models.rarity import Rarity

        rarities = self.catalog_repository.fetch_card_rarities()
        rarity_models = list(map(lambda x: Rarity.from_tcgplayer_response(x), rarities))

        self.catalog_repository.insert_rarities(rarity_models)



