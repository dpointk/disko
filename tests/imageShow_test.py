# tests/image_show_test.py
import unittest
from unittest.mock import patch, MagicMock
import sys
import os
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend'))
sys.path.insert(0, backend_path)
from flask import Flask 
from src.disko.image_management.imageShow import imageShow_bp


class ImageShowBlueprintTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Create a Flask app instance and register the blueprint
        cls.app = Flask(__name__)
        cls.app.register_blueprint(imageShow_bp)
        cls.client = cls.app.test_client()

    @patch('src.disko.image_management.imageShow.SQLiteCRUD')
    def test_get_images_success(self, MockSQLiteCRUD):
        """Test getting images from a valid cluster."""
        mock_db_instance = MockSQLiteCRUD.return_value
        mock_db_instance.select_all.return_value = [
            {'id': 1, 'name': 'Image1'},
            {'id': 2, 'name': 'Image2'}
        ]
        
        # Simulate a GET request to the /api/images/test-cluster endpoint
        response = self.client.get('/api/images/test-cluster')
        
        # Check that the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Check the response data
        self.assertEqual(response.get_json(), [
            {'id': 1, 'name': 'Image1'},
            {'id': 2, 'name': 'Image2'}
        ])
        
        mock_db_instance.select_all.assert_called_once_with('test-cluster')

    @patch('src.disko.image_management.imageShow.SQLiteCRUD')
    def test_get_images_db_error(self, MockSQLiteCRUD):
        """Test handling of a database error."""

        mock_db_instance = MockSQLiteCRUD.return_value
        mock_db_instance.select_all.side_effect = Exception("Database error")
        response = self.client.get('/api/images/test-cluster')
        self.assertEqual(response.status_code, 500)
        
        # Check the response data
        self.assertEqual(response.get_json(), {'error': 'Database error'})

if __name__ == '__main__':
    unittest.main()
