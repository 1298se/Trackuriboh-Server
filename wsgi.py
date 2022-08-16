import asyncio

from dotenv import load_dotenv

from app import create_app, scheduler, db_sync_worker
from config import AppConfig

load_dotenv()
app = create_app(AppConfig)


scheduler.add_job(db_sync_worker.update_card_database, trigger="interval", seconds=1)
scheduler.start()

asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    app.run()
