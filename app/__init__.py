from typing import Union

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from services.db_sync_worker import DatabaseSyncWorker
from repositories.catalog_repository import CatalogRepository
from services.tcgplayer_api_service import TCGPlayerApiService

db = SQLAlchemy()
tcgplayer_api_service = TCGPlayerApiService()
catalog_repository = CatalogRepository()
db_sync_worker = DatabaseSyncWorker()
scheduler = BackgroundScheduler()


def create_app(config: Union[object, str]) -> Flask:
    # Import here to create tables

    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    with app.app_context():
        from models import card, condition, printing, rarity, set, sku
        db.create_all()

    catalog_repository.init(tcgplayer_api_service, db, app.app_context())
    db_sync_worker.init(catalog_repository)
    scheduler.add_job(db_sync_worker.update_card_database, trigger="interval", seconds=5)
    return app
