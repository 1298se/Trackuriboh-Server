import asyncio
from datetime import datetime

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from dotenv import load_dotenv

from app import create_app, scheduler, db_sync_worker, price_sync_worker
from config import AppConfig

load_dotenv()
app = create_app(AppConfig)

initial_db_update_job = scheduler.add_job(db_sync_worker.update_card_database)
scheduler.add_job(db_sync_worker.update_card_database, trigger="interval", hours=12)
scheduler.add_job(price_sync_worker.update_prices, trigger="interval", hours=1)


def price_sync_job_execution_listener(event):
    if event.exception:
        print(f'job id {event.job_id} failed')
    else:
        # check that the executed job is the first job
        if event.job_id == initial_db_update_job.id:
            print('Running price_sync_job')
            scheduler.add_job(price_sync_worker.update_prices)


scheduler.add_listener(price_sync_job_execution_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

scheduler.start()

asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    app.run()
