# import getpass
import docker
from src.disko.image_management.image_controller import *
from src.disko.image_collector import *
from src.disko.sqlite import *
docker_client = docker.from_env()

# # Create db from cluster
# create_db = ImageCollector().collect_images("kind-cluster1")

# # Import sqlite.py to use any function on my db file
# sql = SQLiteCRUD("image_data.db")

# # Import image_controller.py to use any function on my db file
ctl1 = ImageController("image_data.db")

# images = sql.select_all("kind-cluster1")
# images = ["registry.k8s.io/kube-proxy:v1.25.3"]
images = ["python:3.8-slim-bullseye"]

# password = getpass.getpass("Enter your Password: ")
ctl1.copy_images(images, "ygalidan/test1", "3.8-slim-bullseye", "ygalidan", "Ygal3165!")

def test_copy_images():
    docker_client.login("ygalidan", "Ygal3165!")
    pull = docker_client.images.pull("ygalidan/test1", "3.8-slim-bullseye")

    assert pull != ""

