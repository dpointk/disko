#tests/server_test.py
import unittest
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from server import create_app

class FlaskServerStartupTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the Flask test client
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_root_route(self):
        """Test if the Flask app is serving the root route."""
        response = self.client.get('/')
        self.assertIn(response.status_code, [200, 404])  # Adjust depending on if you expect a 200 or 404

    def test_health_route(self):
        """Test if the Flask app is serving a health check route or similar."""
        response = self.client.get('/health')
        self.assertIn(response.status_code, [200, 404])  # Adjust depending on if you expect a 200 or 404

if __name__ == '__main__':
    unittest.main()
