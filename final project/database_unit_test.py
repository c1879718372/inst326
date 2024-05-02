import unittest
from unittest.mock import patch, MagicMock
import database  # Assuming your database functions are in a module named 'database'

class TestDatabase(unittest.TestCase):
    @patch('database.create_connection')
    def test_add_material(self, mock_create_connection):
        # Setup mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_create_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Test add_material function
        database.add_material("Test Book", "Author Name", "Fiction", "SN001", "book")

        # Normalize SQL query for comparison by removing newlines and extra spaces
        expected_query = ' '.join("INSERT INTO materials (title, author, subject, serial_number, type) VALUES (?, ?, ?, ?, ?);".split())
        actual_query = ' '.join(mock_cursor.execute.call_args[0][0].split())

        # Assert cursor.execute was called correctly
        self.assertEqual(expected_query, actual_query)
        self.assertEqual(mock_cursor.execute.call_args[0][1], ("Test Book", "Author Name", "Fiction", "SN001", "book"))

        # Ensure the connection is committed and closed
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('database.create_connection')
    def test_add_user(self, mock_create_connection):
        # Setup mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_create_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Test add_user function
        database.add_user("John Doe", "john@example.com")

        # Normalize SQL query for comparison
        expected_query = ' '.join("INSERT INTO users (name, email) VALUES (?, ?);".split())
        actual_query = ' '.join(mock_cursor.execute.call_args[0][0].split())

        # Assert cursor.execute was called correctly
        self.assertEqual(expected_query, actual_query)
        self.assertEqual(mock_cursor.execute.call_args[0][1], ("John Doe", "john@example.com"))

        # Ensure the connection is committed and closed
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('database.create_connection')
    def test_checkout_item(self, mock_create_connection):
        # Setup mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1  # Mocking rowcount to behave as expected
        mock_create_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Test checkout_item function
        user_id, material_id, days = 1, 1, 14
        database.checkout_item(user_id, material_id, days)

        # Check if execute was called at least once (this is a simplification)
        mock_cursor.execute.assert_called()
        # Ensure the connection is committed and closed
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
