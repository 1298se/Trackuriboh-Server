from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from db_sync_worker import DatabaseSyncWorker
from tcgplayer_request_handler import TCGPlayerRequestHandler
from appconfig import AppConfig

load_dotenv()

db = SQLAlchemy()
tcgplayer_request_handler = TCGPlayerRequestHandler()
database_sync_worker = DatabaseSyncWorker(tcgplayer_request_handler)


def create_app() -> Flask:
    # Import here to create tables
    from models.card import Card
    from models.set import Set
    from models.sku import Sku
    from models.rarity import Rarity
    from models.printing import Printing
    from models.condition import Condition

    flask_app = Flask(__name__)
    flask_app.config.from_object(AppConfig)
    db.init_app(flask_app)
    db.create_all(app=flask_app)

    return flask_app


scheduler = BackgroundScheduler()
scheduler.add_job(func=database_sync_worker.update_card_database, trigger="interval", seconds=5)
scheduler.start()

if __name__ == '__main__':
    app = create_app()
    app.run()
