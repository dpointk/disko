#tests/postReq_test.py
import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import logging

# Suppress lower-level logs (e.g., DEBUG and INFO) from specific modules
logging.getLogger('docker').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

# Add the backend directory to the Python path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend'))
sys.path.insert(0, backend_path)

from flask import Flask
from src.disko.image_management.postReq import postReq_bp
from src.disko.image_management.postReq import getStatRes_bp

class ClusterAPITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.register_blueprint(postReq_bp)
        cls.app.register_blueprint(getStatRes_bp)
        cls.client = cls.app.test_client()

    @patch('src.disko.image_collector.ImageCollector.collect_images')
    def test_select_cluster_success(self, mock_collect_images):
        mock_collect_images.return_value = None
        response = self.client.post('/api/selected-cluster', json={'cluster': 'test-cluster'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': 'Cluster test-cluster selected and processed successfully'})
        mock_collect_images.assert_called_once_with('test-cluster')

    @patch('src.disko.image_collector.ImageCollector.collect_images')
    def test_select_cluster_no_cluster(self, mock_collect_images):
        response = self.client.post('/api/selected-cluster', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {'error': 'No cluster selected'})
        mock_collect_images.assert_not_called()

    @patch('src.disko.image_collector.ImageCollector.collect_images')
    def test_select_cluster_error(self, mock_collect_images):
        with self.assertLogs('root', level='ERROR'):
            mock_collect_images.side_effect = Exception("Processing error")
            response = self.client.post('/api/selected-cluster', json={'cluster': 'test-cluster'})
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.get_json(), {'error': 'Processing error'})

    @patch('src.disko.image_management.image_controller.ImageController.calculate_percentages')
    def test_get_statistics_success(self, mock_calculate_percentages):
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

    @patch('src.disko.image_management.image_controller.ImageController.calculate_percentages')
    def test_get_statistics_no_cluster(self, mock_calculate_percentages):
        response = self.client.get('/api/statistics')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {'error': 'No cluster provided'})
        mock_calculate_percentages.assert_not_called()

    @patch('src.disko.image_management.image_controller.ImageController.calculate_percentages')
    def test_get_statistics_error(self, mock_calculate_percentages):
        with self.assertLogs('root', level='ERROR'):
            mock_calculate_percentages.side_effect = Exception("Calculation error")
            response = self.client.get('/api/statistics', query_string={'cluster': 'test-cluster'})
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.get_json(), {'error': 'Internal Server Error'})

if __name__ == '__main__':
    unittest.main()
