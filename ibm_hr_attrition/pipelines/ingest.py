from pathlib import Path

import pandas as pd
from sqlalchemy import text

from db_utils import ensure_database_exists, get_db_config, get_engine


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def ingest_csv():
    get_db_config()
    ensure_database_exists()
    engine = get_engine()

    csv_path = PROJECT_ROOT / "data" / "raw" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found at {csv_path}")

    df = pd.read_csv(csv_path)

    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))

    df.to_sql(
        "hr_attrition_raw",
        engine,
        schema="raw",
        if_exists="replace",
        index=False,
    )

    print(f"Ingest done: loaded {len(df)} rows into raw.hr_attrition_raw")


if __name__ == "__main__":
    ingest_csv()
