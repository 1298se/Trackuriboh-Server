import os


class AppConfig:
    """Set Flask configuration from .env file."""

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
