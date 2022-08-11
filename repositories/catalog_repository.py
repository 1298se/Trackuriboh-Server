from flask_sqlalchemy import SQLAlchemy

from tcgplayer_api_service import TCGPlayerApiService


class CatalogRepository:

    def __init__(self, api_service: TCGPlayerApiService, db: SQLAlchemy):
        self.api_service = api_service
        self.db = db

    def fetch_card_rarities(self):
        response = self.api_service.get_card_rarities()
        return response['results']

    def insert_rarities(self, rarities):
        self.db.session.add_all(rarities)
        self.db.session.commit()
