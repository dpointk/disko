import unittest
import os
import sys
from unittest.mock import patch, MagicMock
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.mvc.controller import ImageController

class TestImageController(unittest.TestCase):
    @patch('src.mvc.controller.docker.from_env')
    def test_copy_images(self, mock_docker_from_env):
        # Configure the mock to return a mock Docker client
        mock_docker_client = MagicMock()
        mock_docker_from_env.return_value = mock_docker_client

        # Mock the Docker client's methods
        mock_docker_client.login.return_value = True
        mock_docker_client.images.pull.return_value = MagicMock(tag=lambda x: None)
        mock_docker_client.images.push.return_value = True

        # Initialize ImageController instance
        controller = ImageController("image_data.db")

        # Define test data
        images = [("nginx:latest", "2024-03-19 20:29:55", "Dockerhub")]
        new_registry = "dshwartzman5/test-project"
        username = "dshwartzman5"
        password = os.getenv('DOCKER_PASSWORD')

        # Call the function to be tested
        controller.copy_images(images, new_registry, username, password)

        # Verify the image was pulled and pushed
        mock_docker_client.images.pull.assert_called_once_with("nginx")
        mock_docker_client.images.push.assert_called_once_with("dshwartzman5/test-project:1")

if __name__ == "__main__":
    unittest.main()

