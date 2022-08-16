from typing import Union

from aiohttp import ClientSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from repositories.tcgplayer_catalog_repository import TCGPlayerCatalogRepository
from services.db_sync_worker import DatabaseSyncWorker
from services.tcgplayer_api_service import TCGPlayerApiService, TCGPLAYER_BASE_URL

db = SQLAlchemy()
tcgplayer_client_session = ClientSession(TCGPLAYER_BASE_URL)
tcgplayer_api_service = TCGPlayerApiService()
catalog_repository = TCGPlayerCatalogRepository()
db_sync_worker = DatabaseSyncWorker()
scheduler = AsyncIOScheduler()


def create_app(config: Union[object, str]) -> Flask:
    # Import here to create tables

    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    tcgplayer_api_service.init(tcgplayer_client_session)
    catalog_repository.init(tcgplayer_api_service, db, app.app_context())
    db_sync_worker.init(catalog_repository)
    return app
