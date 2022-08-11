from dotenv import load_dotenv
from flask import Flask

from appconfig import AppConfig
from extensions import db
from extensions import scheduler
from extensions import database_sync_worker

load_dotenv()


def create_app() -> Flask:
    # Import here to create tables

    flask_app = Flask(__name__)
    flask_app.config.from_object(AppConfig)
    db.init_app(flask_app)

    with flask_app.app_context():
        db.create_all()

    return flask_app

print(__name__)
if __name__ == '__main__':
    print("RUNNING SHIT")
    app = create_app()
    app.run()
    scheduler.add_job(func=database_sync_worker.update_card_database, trigger="interval", seconds=5)
    scheduler.start()
