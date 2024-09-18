import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the backend directory to the Python path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend'))
sys.path.insert(0, backend_path)

from flask import Flask
from api import api, get_image_controller

class APITestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.register_blueprint(api)  # Register the combined API blueprint
        cls.client = cls.app.test_client()

    @patch('api.ImageController.get_kubernetes_clusters')
    def test_get_clusters(self, mock_get_clusters):
        """Test getting a list of Kubernetes clusters."""
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

    @patch('api.ImageCollector.collect_images')
    def test_select_cluster(self, mock_collect_images):
        """Test selecting a cluster and processing it."""
        mock_collect_images.return_value = None
        response = self.client.post('/api/selected-cluster', json={'cluster': 'test-cluster'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': 'Cluster test-cluster selected and processed successfully'})
        mock_collect_images.assert_called_once_with('test-cluster')

    @patch('api.ImageController.calculate_percentages')
    def test_get_statistics(self, mock_calculate_percentages):
        """Test getting statistics for a cluster."""
        mock_calculate_percentages.return_value = [
            ('registry1', 10, 50.0),
            ('registry2', 10, 50.0)
        ]
        response = self.client.get('/api/statistics', query_string={'cluster': 'test-cluster'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            'results': [
                {'registry': 'registry1', 'amount': 10, 'percentage': 50.0},
                {'registry': 'registry2', 'amount': 10, 'percentage': 50.0}
            ]
        })
        mock_calculate_percentages.assert_called_once_with('test-cluster')

    @patch('api.ImageController.cluster_migration')
    def test_migration(self, mock_cluster_migration):
        """Test migrating a cluster's images to a new registry."""
        mock_cluster_migration.return_value = None
        response = self.client.get('/api/clustermigration', query_string={
            'registry': 'test_registry',
            'tag': 'latest',
            'username': 'user',
            'password': 'pass',
            'helm_chart_path': '/path/to/helm'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': 'Image name replaced successfully in /path/to/helm'})
        mock_cluster_migration.assert_called_once_with(
            'test_registry', 'latest', 'user', 'pass', '/path/to/helm'
        )

    @patch('api.ImageController.present_images_per_cluster')
    def test_get_images(self, mock_present_images):
        """Test getting images for a specific cluster."""
        mock_present_images.return_value = [
            {'id': 1, 'name': 'Image1'},
            {'id': 2, 'name': 'Image2'}
        ]
        response = self.client.get('/api/images/test-cluster')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [
            {'id': 1, 'name': 'Image1'},
            {'id': 2, 'name': 'Image2'}
        ])
        mock_present_images.assert_called_once_with('test-cluster')

    @patch('api.ImageController.copy_images')
    def test_copy_images(self, mock_copy_images):
        """Test copying images to a new registry."""
        mock_copy_images.return_value = None
        response = self.client.get('/api/copyimage', query_string={
            'new_registry': 'test-registry',
            'tag': 'latest',
            'target_username': 'testuser',
            'target_password': 'testpass',
            'images': ['image1', 'image2']
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': 'Images copied successfully!'})
        mock_copy_images.assert_called_once_with(
            ['image1', 'image2'], 'test-registry', 'latest', 'testuser', 'testpass'
        )

if __name__ == '__main__':
    unittest.main()
