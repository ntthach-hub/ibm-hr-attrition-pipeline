import os
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# Load .env located next to this file (optional; fall back to current env)
DOTENV_PATH = Path(__file__).with_name(".env")
if DOTENV_PATH.exists():
    load_dotenv(dotenv_path=DOTENV_PATH, override=True)
else:
    print(f"Warning: .env not found at {DOTENV_PATH}; using existing environment variables.")

def ingest_csv():
    # Kiểm tra các biến môi trường
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    
    if not all([db_user, db_password, db_host, db_port, db_name]):
        raise ValueError(
            "Thiếu biến môi trường! Kiểm tra file .env có đủ các biến:\n"
            f"DB_USER={db_user}\n"
            f"DB_PASSWORD={'***' if db_password else None}\n"
            f"DB_HOST={db_host}\n"
            f"DB_PORT={db_port}\n"
            f"DB_NAME={db_name}"
        )
    
    # URL-encode to handle special chars like @ in password
    safe_user = quote_plus(db_user)
    safe_password = quote_plus(db_password)
    engine = create_engine(
        f"postgresql://{safe_user}:{safe_password}"
        f"@{db_host}:{db_port}/{db_name}"
    )

    csv_path = Path(__file__).parent / "data" / "raw" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found at {csv_path}")

    df = pd.read_csv(csv_path)

    df.to_sql(
        "hr_attrition_raw",
        engine,
        schema="raw",
        if_exists="replace",
        index=False
    )

    print("Ingest done")

if __name__ == "__main__":
    ingest_csv()
