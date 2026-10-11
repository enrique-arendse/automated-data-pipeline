
import psycopg
from unittest.mock import MagicMock

from load import load_posts


def set_database_env(monkeypatch):
    """Provide test database settings without exposing real credentials."""

    monkeypatch.setenv("PGHOST", "localhost")
    monkeypatch.setenv("PGPORT", "5432")
    monkeypatch.setenv("PGDATABASE", "data_pipeline")
    monkeypatch.setenv("PGUSER", "test_user")
    monkeypatch.setenv("PGPASSWORD", "test_password")


def test_empty_posts_do_not_connect_to_database(monkeypatch):
    """An empty list should not open a database connection."""

    set_database_env(monkeypatch)

    connect_mock = MagicMock()
    monkeypatch.setattr("load.psycopg.connect", connect_mock)

    result = load_posts([])

    assert result == 0
    connect_mock.assert_not_called()


def test_load_posts_creates_table_and_inserts_records(monkeypatch):
    """Valid records should trigger table creation and insertion."""

    set_database_env(monkeypatch)

    # Simulate the database connection and cursor.
    connection = MagicMock()
    connection.__enter__.return_value = connection

    cursor = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    connect_mock = MagicMock(return_value=connection)
    monkeypatch.setattr("load.psycopg.connect", connect_mock)

    posts = [
        {
            "post_id": 1,
            "user_id": 10,
            "title": "Example title",
            "body": "Example body",
        }
    ]

    result = load_posts(posts)

    assert result == 1
    connect_mock.assert_called_once()

    # Check that the loader attempts to create the table.
    cursor.execute.assert_called_once()
    assert "CREATE TABLE IF NOT EXISTS posts" in (
        cursor.execute.call_args[0][0]
    )

    # Check that the record is passed to the insert operation.
    cursor.executemany.assert_called_once()

    inserted_rows = cursor.executemany.call_args[0][1]

    assert inserted_rows == [
        (1, 10, "Example title", "Example body")
    ]


def test_database_connection_failure_is_raised(monkeypatch):
    """Connection failures should not be silently swallowed."""

    set_database_env(monkeypatch)

    def mock_connect(**kwargs):
        raise psycopg.OperationalError("Database unavailable")

    monkeypatch.setattr("load.psycopg.connect", mock_connect)

    posts = [
        {
            "post_id": 1,
            "user_id": 10,
            "title": "Example title",
            "body": "Example body",
        }
    ]

    try:
        load_posts(posts)
    except psycopg.OperationalError as error:
        assert "Database unavailable" in str(error)
    else:
        raise AssertionError(
            "Expected a database connection error."
        )
