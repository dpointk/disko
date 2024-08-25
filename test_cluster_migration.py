# --------------------------------------------- Test intro --------------------------------------------- #
# This test script checks the functionality of the cluster_migration method in the ImageController class:
# 1. test_cluster_mirgation: Verifies that after migrating the cluster, the image in the 
#    values.yaml file is correctly updated to ygalidan/test2.
# 2. test_cluster_migration_pull: Confirms that the updated image (ygalidan/test2:1) can be 
#    successfully pulled from Docker Hub, ensuring the migration was successful.
# --------------------------------------------- Test intro --------------------------------------------- #

from src.disko.image_collector import *
import getpass
import os
import docker
docker_client = docker.from_env()

# Import image_controller.py to use any function
ctl1 = ImageController("")

# Get password from GitHub secret
password = os.getenv("DOCKERHUB_PASSWORD")

ctl1.cluster_migration("ygalidan/test2", "1", "ygalidan", password, "apphelm")

# Define the path to the YAML configuration file for Helm.
yml_values = os.path.join("apphelm/values.yaml")

# Get the current image name from the YAML file.
image = ctl1.get_current_image(yml_values)[0]

# Function to test the correctness of the image name after migration
def test_cluster_mirgation():
    assert image == "ygalidan/test2"

# Function to test if the migrated image can be pulled from Docker Hub
def test_cluster_migration_pull():
    pull = docker_client.images.pull(image, "1")
    assert pull is not None