from typing import Any

from flask.ctx import AppContext
from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy.dialects.mysql import insert

from services.tcgplayer_api_service import TCGPlayerApiService


class CatalogRepository:

    def __init__(self):
        self.app_context = None
        self.db = None
        self.api_service = None

    def init(self, api_service: TCGPlayerApiService, db: SQLAlchemy, app_context: AppContext):
        self.api_service = api_service
        self.db = db
        self.app_context = app_context

    def fetch_card_rarities(self):
        response = self.api_service.get_card_rarities()
        return response['results']

    def fetch_card_printings(self):
        response = self.api_service.get_card_printings()
        return response['results']

    def fetch_card_conditions(self):
        response = self.api_service.get_card_conditions()
        return response['results']

    def insert_printings(self, printings):
        self._insert_if_not_exists(printings)

    def insert_conditions(self, conditions):
        self._insert_if_not_exists(conditions)

    def insert_rarities(self, rarities):
        self._insert_if_not_exists(rarities)

    def _insert_if_not_exists(self, models: list[Model]):
        with self.app_context:
            for model in models:
                if hasattr(model, 'id'):
                    existing_model = model.__class__.query.filter_by(id=model.id).first()

                    if existing_model is None:
                        self.db.session.add(model)

            self.db.session.commit()
