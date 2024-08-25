from src.disko.image_collector import *
import getpass
import os
import docker
docker_client = docker.from_env()

# Create db from cluster
create_db = ImageCollector().collect_images("kind-cluster1")

# Import image_controller.py to use any function on my db file
ctl1 = ImageController("image_data.db")

password = os.getenv("DOCKERHUB_PASSWORD")
ctl1.cluster_migration("ygalidan/test2", "1", "ygalidan", password, "apphelm")
yml_values = os.path.join("apphelm/values.yaml")
image = ctl1.get_current_image(yml_values)[0]

def test_cluster_mirgation():
    assert image == "ygalidan/test2"

def test_cluster_migration_pull():
    pull = docker_client.images.pull(image, "1")
    assert pull is not None