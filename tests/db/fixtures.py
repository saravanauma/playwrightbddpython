import pytest
import psycopg2
import mysql.connector
from psycopg2.extras import RealDictCursor
from tests.utils.config import CURRENT_DB_CONFIG

# =========================================================
# Universal DB Connection Fixture
# =========================================================


@pytest.fixture(scope="session")
def db_connection():
    """
    Creates a database connection based on CURRENT_DB_CONFIG.
    Supports PostgreSQL and MySQL. Closes automatically after tests.
    """
    db_type = CURRENT_DB_CONFIG.get("type", "postgres").lower()
    conn = None

    try:
        if db_type == "postgres":
            conn = psycopg2.connect(
                host=CURRENT_DB_CONFIG["host"],
                port=CURRENT_DB_CONFIG["port"],
                user=CURRENT_DB_CONFIG["user"],
                password=CURRENT_DB_CONFIG["password"],
                database=CURRENT_DB_CONFIG["database"],
                cursor_factory=RealDictCursor
            )
        elif db_type == "mysql":
            conn = mysql.connector.connect(
                host=CURRENT_DB_CONFIG["host"],
                port=CURRENT_DB_CONFIG["port"],
                user=CURRENT_DB_CONFIG["user"],
                password=CURRENT_DB_CONFIG["password"],
                database=CURRENT_DB_CONFIG["database"],
                ssl_disabled=False
            )
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

        print(
            f"\n✅ Connected to {db_type.upper()} database: {CURRENT_DB_CONFIG['database']}")
        yield conn

    except Exception as e:
        pytest.skip(f"❌ Database connection failed: {e}")

    finally:
        if conn:
            conn.close()
            print(f"🔒 Closed {db_type.upper()} database connection.")


# =========================================================
# Cursor Fixture (auto-cleanup per test)
# =========================================================
@pytest.fixture
def db_cursor(db_connection):
    """
    Provides a database cursor for executing queries.
    Automatically commits or rolls back after each test.
    """
    cursor = db_connection.cursor()
    try:
        yield cursor
        db_connection.commit()
    except Exception as e:
        db_connection.rollback()
        raise e
    finally:
        cursor.close()
