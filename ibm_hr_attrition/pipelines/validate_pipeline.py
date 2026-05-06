from sqlalchemy import text

from db_utils import get_engine


def validate_pipeline():
    checks = [
        ("raw.hr_attrition_raw", "SELECT COUNT(*) FROM raw.hr_attrition_raw"),
        ("staging.hr_attrition_clean", "SELECT COUNT(*) FROM staging.hr_attrition_clean"),
        ("analytics.attrition_summary", "SELECT COUNT(*) FROM analytics.attrition_summary"),
    ]

    engine = get_engine()
    with engine.connect() as conn:
        for table_name, sql in checks:
            row_count = conn.execute(text(sql)).scalar_one()
            print(f"{table_name}: {row_count} rows")


if __name__ == "__main__":
    validate_pipeline()
