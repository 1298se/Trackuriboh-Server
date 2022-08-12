from repositories.catalog_repository import CatalogRepository


class DatabaseSyncWorker:
    def __init__(self):
        self.catalog_repository = None

    def init(self, catalog_repository: CatalogRepository):
        self.catalog_repository = catalog_repository

    def update_card_database(self):
        from models.condition import Condition
        from models.rarity import Rarity
        from models.printing import Printing

        rarities = self.catalog_repository.fetch_card_rarities()
        rarity_models = list(map(lambda x: Rarity.from_tcgplayer_response(x), rarities))
        print(rarity_models)
        self.catalog_repository.insert_rarities(rarity_models)

        conditions = self.catalog_repository.fetch_card_conditions()
        condition_models = list(map(lambda x: Condition.from_tcgplayer_response(x), conditions))
        print(condition_models)
        self.catalog_repository.insert_conditions(condition_models)

        printings = self.catalog_repository.fetch_card_printings()
        printing_models = list(map(lambda x: Printing.from_tcgplayer_response(x), printings))
        print(printing_models)
        self.catalog_repository.insert_printings(printing_models)





