import pytest
from unittest.mock import patch, MagicMock


# @pytest.fixture(autouse=True)
# def mock_db_connection():
#     with patch("app.utils.db_driver.get_conn_and_cursor") as mock_conn:
#         mock_cursor = MagicMock()
#         mock_conn.return_value = (MagicMock(), mock_cursor)
#         print("Mocked get_conn_and_cursor")
#         yield


# @pytest.fixture(autouse=True)
# def mock_mysql_connector():
#     with patch("mysql.connector.connect", return_value=MagicMock()) as mock_connect:
#         print("Mocked mysql.connector.connect")
#         yield
