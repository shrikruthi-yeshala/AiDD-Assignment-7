import os
import sys
import pytest
from pathlib import Path

# Ensure project root is on sys.path so tests can import project modules like `DAL`.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import DAL as dal


@pytest.fixture
def client(tmp_path):
    """Create a Flask test client that uses a temporary SQLite DB.

    This fixture patches DAL._DB_PATH to point at a temp file inside tmp_path
    so tests do not touch the repository database.
    """
    test_db = tmp_path / "projects_test.db"
    # Point DAL at the test DB path and initialize an empty DB
    dal._DB_PATH = test_db
    dal.initialize_database(seed_with_examples=False)

    # Import the Flask app and create a test client
    from app import app as flask_app

    flask_app.config.update(TESTING=True)

    with flask_app.test_client() as client:
        yield client


@pytest.fixture
def dal_module():
    """Expose the DAL module for tests to perform DB operations directly."""
    return dal
