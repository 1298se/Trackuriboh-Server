import asyncio

from dotenv import load_dotenv

from app import create_app, scheduler, db_sync_worker, price_sync_worker
from config import AppConfig

load_dotenv()
app = create_app(AppConfig)

initial_db_update_job = scheduler.add_job(db_sync_worker.update_card_database)
scheduler.add_job(db_sync_worker.update_card_database, trigger="interval", hours=12)
scheduler.add_job(price_sync_worker.update_prices, trigger="cron", hour="*/6")


scheduler.start()

asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    app.run()
