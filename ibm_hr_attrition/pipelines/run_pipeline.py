import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# Load .env
DOTENV_PATH = Path(__file__).with_name(".env")
if DOTENV_PATH.exists():
    load_dotenv(dotenv_path=DOTENV_PATH, override=True)
else:
    print(f"Warning: .env not found at {DOTENV_PATH}")

def run_transfrom():
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    
    # URL-encode to handle special chars
    safe_user = quote_plus(db_user)
    safe_password = quote_plus(db_password)
    
    engine = create_engine(
        f"postgresql+psycopg2://{safe_user}:{safe_password}@{db_host}:{db_port}/{db_name}"
    )

    sql_files = [
        "sql/create_schema.sql",
        "sql/transform_raw_to_staging.sql",
        "sql/analytics.sql"
    ]

    with engine.connect() as conn:
        for file in sql_files:
            print(f"Running {file}")
            with open(file, "r", encoding="utf-8") as f:
                conn.execute(text(f.read()))
            conn.commit()

    print("Pipeline finished")
