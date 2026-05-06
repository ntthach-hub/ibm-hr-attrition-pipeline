from pathlib import Path

from sqlalchemy import text

from db_utils import get_engine


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_transform():
    engine = get_engine()
    sql_files = [
        PROJECT_ROOT / "sql" / "create_schema.sql",
        PROJECT_ROOT / "sql" / "transform_raw_to_staging.sql",
        PROJECT_ROOT / "sql" / "analytics.sql",
    ]

    with engine.connect() as conn:
        for file in sql_files:
            print(f"Running {file}")
            with open(file, "r", encoding="utf-8") as f:
                conn.execute(text(f.read()))
            conn.commit()

    print("Pipeline finished")


def run_transfrom():
    return run_transform()
