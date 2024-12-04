import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture(autouse=True)
def mock_db_connection():
    with patch("app.utils.db_driver.get_conn_and_cursor") as mock_conn:
        mock_cursor = MagicMock()
        mock_conn.return_value = (MagicMock(), mock_cursor)
        yield
