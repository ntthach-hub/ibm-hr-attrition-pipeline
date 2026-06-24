from sqlalchemy import text

from db_utils import get_engine


def validate_pipeline():
    engine = get_engine()
    with engine.connect() as conn:

        # --- CHECK 1: Đếm số dòng (bạn đã có) ---
        checks = [
            ("raw.hr_attrition_raw", "SELECT COUNT(*) FROM raw.hr_attrition_raw"),
            ("staging.hr_attrition_clean", "SELECT COUNT(*) FROM staging.hr_attrition_clean"),
            ("analytics.attrition_summary", "SELECT COUNT(*) FROM analytics.attrition_summary"),
        ]
        for table_name, sql in checks:
            row_count = conn.execute(text(sql)).scalar_one()
            print(f"{table_name}: {row_count} rows")

        # --- CHECK 2: Staging không được có NULL ở cột quan trọng ---
        null_count = conn.execute(text("""
            SELECT COUNT(*) FROM staging.hr_attrition_clean
            WHERE age IS NULL OR attrition IS NULL OR department IS NULL
        """)).scalar_one()
        assert null_count == 0, f" Staging có {null_count} dòng NULL!"
        print(" Không có NULL ở cột quan trọng")

        # --- CHECK 3: Attrition chỉ được có Yes/No ---
        invalid_attrition = conn.execute(text("""
            SELECT COUNT(*) FROM staging.hr_attrition_clean
            WHERE attrition NOT IN ('Yes', 'No')
        """)).scalar_one()
        assert invalid_attrition == 0, f" Attrition có {invalid_attrition} giá trị lạ!"
        print(" Attrition chỉ có Yes/No")
        # --- CHECK 4: Số dòng staging phải bằng raw ---
        raw_count = conn.execute(text(
            "SELECT COUNT(*) FROM raw.hr_attrition_raw"
        )).scalar_one()
        staging_count = conn.execute(text(
            "SELECT COUNT(*) FROM staging.hr_attrition_clean"
        )).scalar_one()
        assert staging_count == raw_count, \
            f" Staging ({staging_count}) != Raw ({raw_count}), bị mất dòng!"
        print("Số dòng staging khớp với raw")

        print("\n Tất cả validate passed!")

if __name__ == "__main__":
    validate_pipeline()
