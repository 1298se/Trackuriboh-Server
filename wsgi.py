from dotenv import load_dotenv

from app import create_app, scheduler
from config import AppConfig

load_dotenv()
app = create_app(AppConfig)

scheduler.start()

if __name__ == '__main__':
    print("RUNNING SHIT")
    app.run()
