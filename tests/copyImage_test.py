import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the backend directory to the Python path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend'))
sys.path.insert(0, backend_path)

from flask import Flask
from src.disko.image_management.copyImage import copyimage_bp

class CopyImageBlueprintTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Create a Flask app instance and register the blueprint
        cls.app = Flask(__name__)
        cls.app.register_blueprint(copyimage_bp)
        cls.client = cls.app.test_client()

    @patch('src.disko.image_management.image_controller.ImageController.copy_images')
    @patch('src.disko.image_management.image_controller.ImageController.__init__', return_value=None)
    def test_copy_images_success(self, mock_init, mock_copy_images):
        """Test successful image copy."""
        # Set up mock return value for copy_images
        mock_copy_images.return_value = None
        
        # Simulate a GET request with query parameters
        response = self.client.get('/api/copyimage', query_string={
            'new_registry': 'test-registry',
            'tag': 'latest',
            'target_username': 'testuser',
            'target_password': 'testpass',
            'images': ['image1', 'image2']
        })
        
        # Check the response status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': 'Images copied successfully!'})
        
        # Ensure that copy_images was called with the correct arguments
        mock_copy_images.assert_called_once_with(
            ['image1', 'image2'], 'test-registry', 'latest', 'testuser', 'testpass'
        )

    @patch('src.disko.image_management.image_controller.ImageController.copy_images')
    @patch('src.disko.image_management.image_controller.ImageController.__init__', return_value=None)
    def test_copy_images_error(self, mock_init, mock_copy_images):
        """Test image copy failure."""
        # Set up mock to raise an exception
        mock_copy_images.side_effect = Exception("Copy failed")
        
        # Simulate a GET request with query parameters
        response = self.client.get('/api/copyimage', query_string={
            'new_registry': 'test-registry',
            'tag': 'latest',
            'target_username': 'testuser',
            'target_password': 'testpass',
            'images': ['image1', 'image2']
        })
        
        # Check the response status code and message
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json(), {'message': 'Copy failed'})

if __name__ == '__main__':
    unittest.main()
