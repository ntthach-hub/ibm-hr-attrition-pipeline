import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


DOTENV_PATH = Path(__file__).with_name(".env")
if DOTENV_PATH.exists():
    load_dotenv(dotenv_path=DOTENV_PATH, override=True)


def get_db_config():
    config = {
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "database": os.getenv("DB_NAME"),
    }
    missing = [key for key, value in config.items() if not value]
    if missing:
        raise ValueError(f"Missing database config: {', '.join(missing)}")
    return config


def build_db_url(database=None, driver="postgresql+psycopg2"):
    config = get_db_config()
    db_name = database or config["database"]
    safe_user = quote_plus(config["user"])
    safe_password = quote_plus(config["password"])
    return (
        f"{driver}://{safe_user}:{safe_password}"
        f"@{config['host']}:{config['port']}/{db_name}"
    )


def get_engine(database=None):
    return create_engine(build_db_url(database=database))


def ensure_database_exists():
    config = get_db_config()
    admin_engine = get_engine(database="postgres")

    with admin_engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
            {"db_name": config["database"]},
        ).scalar()
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{config["database"]}"'))
            print(f"Created database {config['database']}")
