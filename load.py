
import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


def load_posts(posts):
    """Create the posts table and load validated records."""

    # 1. Read the database settings.
    required_settings = [
        "PGHOST",
        "PGPORT",
        "PGDATABASE",
        "PGUSER",
        "PGPASSWORD",
    ]

    settings = {
        setting: os.getenv(setting)
        for setting in required_settings
    }

    # 2. Check that all required settings exist.
    missing_settings = [
        setting
        for setting, value in settings.items()
        if not value
    ]

    if missing_settings:
        raise ValueError(
            f"Missing database settings: {missing_settings}"
        )

    # 3. Validate and convert the port.
    port_value = settings["PGPORT"]

    if port_value is None:
        raise ValueError(
            "Missing required database setting: PGPORT"
        )

    try:
        port = int(port_value)
    except ValueError as exc:
        raise ValueError(
            "PGPORT must be a valid integer."
        ) from exc

    if not 1 <= port <= 65535:
        raise ValueError(
            "PGPORT must be between 1 and 65535."
        )

    # 4. Stop if there are no records to load.
    if not posts:
        print("No valid records to load.")
        return 0

    # 5. Insert records, updating existing post IDs.
    insert_sql = """
        INSERT INTO posts (post_id, user_id, title, body)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (post_id) DO UPDATE SET
            user_id = EXCLUDED.user_id,
            title = EXCLUDED.title,
            body = EXCLUDED.body;
    """

    # 6. Connect to PostgreSQL and create the table if needed.
    with psycopg.connect(
        host=settings["PGHOST"],
        port=port,
        dbname=settings["PGDATABASE"],
        user=settings["PGUSER"],
        password=settings["PGPASSWORD"],
    ) as connection:

        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    post_id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    body TEXT NOT NULL
                );
            """)

            rows = [
                (
                    post["post_id"],
                    post["user_id"],
                    post["title"],
                    post["body"],
                )
                for post in posts
            ]

            cursor.executemany(insert_sql, rows)

    print(f"Loaded {len(posts)} valid records.")

    return len(posts)