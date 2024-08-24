#tests/clusters_test.py
import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import logging

# Add the backend directory to the Python path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend'))
sys.path.insert(0, backend_path)

from flask import Flask
from src.disko.image_management.clusters import cluster_bp  # Adjust the import path based on your structure

class ClusterBlueprintTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.register_blueprint(cluster_bp)
        cls.client = cls.app.test_client()

    @patch('src.disko.image_management.image_controller.ImageController.get_kubernetes_clusters')
    @patch('src.disko.image_management.image_controller.ImageController.__init__', return_value=None)
    def test_get_clusters_success(self, mock_init, mock_get_clusters):
        """Test successfully retrieving Kubernetes clusters."""
        mock_get_clusters.return_value = [
            {'name': 'cluster1', 'status': 'active'},
            {'name': 'cluster2', 'status': 'inactive'}
        ]
        response = self.client.get('/api/clusters')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [
            {'name': 'cluster1', 'status': 'active'},
            {'name': 'cluster2', 'status': 'inactive'}
        ])
        mock_get_clusters.assert_called_once()

    @patch('src.disko.image_management.image_controller.ImageController.get_kubernetes_clusters')
    @patch('src.disko.image_management.image_controller.ImageController.__init__', return_value=None)
    def test_get_clusters_error(self, mock_init, mock_get_clusters):
        """Test handling of an error during cluster retrieval."""
        mock_get_clusters.side_effect = Exception("Error retrieving clusters")
        
        # Temporarily disable logging during this test
        logging.disable(logging.CRITICAL)
        try:
            response = self.client.get('/api/clusters')
            self.assertEqual(response.status_code, 500)
            self.assertIsNone(response.get_json())
        finally:
            # Re-enable logging after the test
            logging.disable(logging.NOTSET)

if __name__ == '__main__':
    unittest.main()
