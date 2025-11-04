import os
import pytest
import psycopg2
import mysql.connector
from tests.utils.config import CURRENT_DB_CONFIG
from tests.utils.logger import logger

# Skip all tests in this module if DB config is missing required values
pytestmark = pytest.mark.skipif(
    not all(CURRENT_DB_CONFIG.get(key)
            for key in ['host', 'port', 'user', 'password', 'database']),
    reason=f"Missing required database configuration. Check environment variables for DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME. Current ENV={os.getenv('ENV', 'pre_staging')}"
)


def test_db_connection_successful(db_connection):
    """Test that database connection can be established successfully."""
    # Log connection details (masking sensitive data)
    safe_config = {
        k: ('****' if k in ['password', 'pass'] else v)
        for k, v in CURRENT_DB_CONFIG.items()
    }
    logger.info("Testing database connection for environment %s",
                os.getenv('ENV', 'pre_staging'))
    logger.info("Database configuration: %s", safe_config)

    assert db_connection is not None, "Database connection should not be None"

    # Test that we can execute a simple query
    with db_connection.cursor() as cursor:
        try:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            assert result is not None, "Should be able to execute a simple query"
            logger.info("Successfully executed test query")
        except Exception as e:
            logger.error("Failed to execute test query: %s", e)
            raise
