import unittest
from unittest.mock import patch
from library_management import checkout_item, return_item, search_materials

class TestLibraryManagementSystem(unittest.TestCase):
    def setUp(self):
        # Setup that will be performed before each test
        pass

    @patch('library_management.checkout_item')
    def test_checkout_item_failure(self, mock_checkout):
        # Test failed checkout
        mock_checkout.return_value = False
        self.assertFalse(checkout_item(1, 100))

    @patch('library_management.return_item')
    def test_return_item(self, mock_return):
        # Test return item
        mock_return.return_value = None
        self.assertIsNone(return_item(100))

    @patch('library_management.search_materials')
    def test_search_materials_found(self, mock_search):
        # Assuming search_materials returns a list of tuples with detailed info
        mock_search.return_value = [(1, 'The Great Gatsby', 'F. Scott Fitzgerald', 'American Literature', 'SN12345', 'book', 'available')]
        expected_result = [(1, 'The Great Gatsby', 'F. Scott Fitzgerald', 'American Literature', 'SN12345', 'book', 'available')]
        self.assertEqual(search_materials('Gatsby'), expected_result)


    @patch('library_management.search_materials')
    def test_search_materials_not_found(self, mock_search):
        # Test searching materials when no items are found
        mock_search.return_value = []
        self.assertEqual(search_materials('Unknown'), [])

if __name__ == '__main__':
    unittest.main()
