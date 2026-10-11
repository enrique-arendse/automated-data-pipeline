# Automated Data Pipeline: API to PostgreSQL

## Overview

This project is a Python-based data engineering pipeline that extracts data from a public REST API, validates and transforms the records, and loads the cleaned data into a PostgreSQL database.

The project demonstrates core data engineering concepts, including API integration, data validation, database loading, automated testing, logging, and scheduled execution.

## Project Objectives

- Extract records from an external API.
- Validate required fields and reject invalid or duplicate records.
- Transform API responses into a database-friendly structure.
- Load validated records into PostgreSQL.
- Use automated tests to verify pipeline behaviour.
- Record execution details in a log file.
- Schedule automatic execution using Windows Task Scheduler.

## Architecture

The pipeline follows an Extract, Transform, Load (ETL) approach.

1. **Extract:** Retrieve post records from the JSONPlaceholder public API.
2. **Transform:** Validate records, clean text fields, and separate valid records from rejected records.
3. **Load:** Insert validated records into PostgreSQL.
4. **Monitor:** Record pipeline progress and errors in a log file.
5. **Automate:** Run the pipeline on a schedule using Windows Task Scheduler.

```text
JSONPlaceholder API
        |
        v
    extract.py
        |
        v
    transform.py
        |
        +---- Valid records
        |          |
        |          v
        |       load.py
        |          |
        |          v
        |      PostgreSQL
        |
        +---- Rejected records
                   |
                   v
              Pipeline logs

main.py coordinates the pipeline.
pytest tests the pipeline components.
Windows Task Scheduler runs the pipeline automatically.
```

## Technologies Used

- **Python** — pipeline implementation and data processing.
- **Requests** — HTTP requests to the public API.
- **PostgreSQL** — relational database for storing records.
- **Psycopg** — Python-to-PostgreSQL connectivity.
- **python-dotenv** — loading configuration from environment variables.
- **pytest** — automated testing.
- **Git and GitHub** — version control and project hosting.
- **Windows Task Scheduler** — scheduled pipeline execution.

## Project Structure

```text
data-pipeline-project/
├── tests/
│   ├── test_transform.py
│   ├── test_extract.py
│   └── test_load.py
├── logs/
│   └── pipeline.log
├── .gitignore
├── .env                 # Local only; never commit
├── requirements.txt
├── extract.py
├── transform.py
├── load.py
├── main.py
└── README.md
```

## Prerequisites

Before running the project, install:

- Python
- PostgreSQL
- Git (for version control)

You will also need internet access to retrieve data from the public API.

## Setup Instructions

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd data-pipeline-project
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the actual repository URL.

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the Python executable directly from `.venv\Scripts\python.exe` instead.

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Create the PostgreSQL database

Create a database named `data_pipeline` in PostgreSQL if it does not already exist.

The pipeline creates the `posts` table when records are loaded.

### 5. Configure environment variables

Create a local `.env` file in the project root:

```dotenv
PGHOST=localhost
PGPORT=5432
PGDATABASE=data_pipeline
PGUSER=your_postgres_username
PGPASSWORD=your_postgres_password
```

Replace the username and password with your own PostgreSQL credentials.

**Security:** Never commit `.env` or publish database passwords.

### 6. Run the pipeline

```powershell
python main.py
```

The pipeline extracts API data, validates it, loads valid records into PostgreSQL, and logs its execution.

### 7. Run the automated tests

```powershell
python -m pytest -v
```

The tests cover extraction behaviour, transformation and validation, and simulated database-loading operations.

## Database Design

The pipeline creates a `posts` table with these columns:

| Column | Type | Purpose |
|---|---|---|
| `post_id` | INTEGER | Primary key identifying each post |
| `user_id` | INTEGER | Identifies the user associated with the post |
| `title` | TEXT | Post title |
| `body` | TEXT | Post content |

The loader uses an upsert operation with `ON CONFLICT (post_id) DO UPDATE`. This updates existing records when the same post ID is loaded again rather than inserting a second row with that ID.

## Logging and Automation

Pipeline execution details are written to `logs/pipeline.log`, including record counts and failures.

Windows Task Scheduler is configured to execute the pipeline periodically using the Python executable in the project's virtual environment.

The computer must be available at the scheduled time for the task to run, unless appropriate wake and task conditions have been configured.

## Testing

The automated tests use pytest to check expected behaviour without relying on live API calls or making real database changes in the database-loading unit tests.

The test suite currently contains 12 tests covering:

- Successful extraction
- HTTP and connection errors
- Required-field validation
- Cleaning text fields
- Invalid and duplicate record rejection
- Empty input
- Database connection and loading behaviour

Run all tests with:

```powershell
python -m pytest -v
```

## Future Improvements

Potential next steps include:

- Add retry logic for temporary API or database failures.
- Record rejected records in a dedicated database table.
- Add structured logging and log rotation.
- Introduce a dedicated test database for integration testing.
- Add data-quality metrics and pipeline execution summaries.
- Containerise the application with Docker.
- Add continuous integration to run tests automatically on GitHub.

## Learning Outcomes

This project provides practical experience with API integration, Python data processing, SQL databases, data validation, testing, error handling, logging, automation, and version control.
