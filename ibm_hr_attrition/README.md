# IBM HR Attrition Pipeline

## Overview
This project is a small end-to-end data pipeline for the IBM HR Attrition dataset.

The goal is to move HR data from a raw CSV file into PostgreSQL, organize it into data layers, and make it ready for downstream analytics or machine learning work.

## Project Goal
This project is designed to show two things:

1. A simple data engineering workflow:
- ingest raw data
- store data in PostgreSQL
- transform data into cleaner layers
- validate the final output

2. A data science-ready foundation:
- keep the raw source untouched
- create a cleaned staging table
- create an analytics summary table
- expose the data for notebooks and later modeling

## Architecture
`CSV -> raw -> staging -> analytics`

## Tech Stack
- Python
- PostgreSQL
- pandas
- SQLAlchemy
- psycopg2

## Project Structure
```text
ibm_hr_attrition/
|-- data/
|   `-- raw/
|       `-- WA_Fn-UseC_-HR-Employee-Attrition.csv
|-- notebooks/
|   `-- hr_attrition_postgres_walkthrough.ipynb
|-- pipelines/
|   |-- .env
|   |-- db_utils.py
|   |-- ingest.py
|   |-- main.py
|   |-- run_pipeline.py
|   `-- validate_pipeline.py
|-- sql/
|   |-- analytics.sql
|   |-- create_schema.sql
|   `-- transform_raw_to_staging.sql
|-- requirements.txt
`-- README.md
```

## Data Layers
### `raw`
Stores the original dataset loaded from CSV into PostgreSQL.

Table:
- `raw.hr_attrition_raw`

### `staging`
Stores cleaned and selected columns for downstream analysis.

Table:
- `staging.hr_attrition_clean`

### `analytics`
Stores aggregated outputs for quick analysis.

Table:
- `analytics.attrition_summary`

## Database Configuration
Set database credentials in:

`ibm_hr_attrition/pipelines/.env`

Example:

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=hr_data
```

## How To Run
From the repository root:

```powershell
.\.venv\Scripts\python.exe ibm_hr_attrition\pipelines\main.py
```

This script will:

1. Create the target database if it does not exist
2. Load the CSV into `raw.hr_attrition_raw`
3. Run SQL transformations for `staging` and `analytics`
4. Print row-count checks for the final tables

Expected output:

```text
Ingest done: loaded 1470 rows into raw.hr_attrition_raw
Running ...create_schema.sql
Running ...transform_raw_to_staging.sql
Running ...analytics.sql
Pipeline finished
raw.hr_attrition_raw: 1470 rows
staging.hr_attrition_clean: 1470 rows
analytics.attrition_summary: 6 rows
```

## How To View Data In pgAdmin
If you do not see tables immediately, refresh the database tree first.

In pgAdmin:

1. Right click `hr_data` and choose `Refresh`
2. Open `Schemas`
3. Open one of these schemas:
- `raw`
- `staging`
- `analytics`
4. Open `Tables`
5. Right click a table and choose `View/Edit Data` -> `All Rows`

Expected tables:
- `raw.hr_attrition_raw`
- `staging.hr_attrition_clean`
- `analytics.attrition_summary`

## Notebook
Use this notebook for quick inspection from PostgreSQL:

`ibm_hr_attrition/notebooks/hr_attrition_postgres_walkthrough.ipynb`

The notebook:
- connects to PostgreSQL
- checks row counts
- previews raw and staging data
- reads the analytics summary table

## Important Pipeline Files
- `pipelines/db_utils.py`: database config, connection string, engine creation, and database auto-creation
- `pipelines/ingest.py`: reads CSV and loads it into PostgreSQL
- `pipelines/run_pipeline.py`: runs SQL scripts in order
- `pipelines/validate_pipeline.py`: validates final row counts
- `pipelines/main.py`: orchestrates the full pipeline

## Notes
- PostgreSQL is not only for visualization. It is the actual storage and transformation layer in this project.
- The notebook and pgAdmin only read from the database after the pipeline writes data into it.
- This project is suitable as a DS + DE portfolio starter, especially before adding EDA and modeling notebooks.
