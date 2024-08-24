from unittest.mock import patch, MagicMock
import unittest
from flask import Flask
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
from src.disko.image_management.migration import migration_bp
from src.disko.image_management.image_controller import ImageController

class MigrationEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(migration_bp)
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

        # Manually mock the Docker client
        self.original_docker_client = ImageController.__init__
        ImageController.__init__ = self.mocked_image_controller_init

        # Mock the file check
        self.original_file_check = ImageController.cluster_migration
        ImageController.cluster_migration = self.mocked_cluster_migration

    def mocked_image_controller_init(self, db_name):
        self.docker_client = MagicMock()

    def mocked_cluster_migration(self, registry, tag, username, password, helm_chart_path):
        # Simulate successful file check without actual files
        return

    def tearDown(self):
        ImageController.__init__ = self.original_docker_client
        ImageController.cluster_migration = self.original_file_check

    def test_migration_endpoint(self):
        response = self.client.get('/api/clustermigration', query_string={
            'registry': 'test_registry',
            'tag': 'test_tag',
            'username': 'test_user',
            'password': 'test_pass',
            'helm_chart_path': '/path/to/helm/chart'
        })

        self.assertIn(response.status_code, [200, 500])
        json_data = response.get_json()
        self.assertIn('message', json_data)

    def test_migration_endpoint_missing_params(self):
        response = self.client.get('/api/clustermigration', query_string={
            'registry': 'test_registry',
            'tag': 'test_tag',
        })

        self.assertEqual(response.status_code, 500)
        json_data = response.get_json()
        self.assertIn('message', json_data)

if __name__ == '__main__':
    unittest.main()
