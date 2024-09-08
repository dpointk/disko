# ------------------------------------------ Test intro ------------------------------------------ #
# The test verifies that the copy_images method in the ImageController class successfully copies a 
# Docker image (python:3.8-slim-bullseye) to a new repository (ygalidan/test1). It then checks 
# that the copied image can be pulled from Docker Hub, confirming the image was correctly copied 
# and uploaded.
# ------------------------------------------ Test intro ------------------------------------------ #

from src.disko.image_collector import *
import os
import docker
docker_client = docker.from_env()

# Import image_controller.py to use any function
ctl1 = ImageController("")

# Get password from GitHub secret
password = os.getenv("DOCKERHUB_PASSWORD")

# Name of image fron Docker Hub
images = ["python:3.8-slim-bullseye"]

ctl1.copy_images(images, "ygalidan/test1", "3.8-slim-bullseye", "ygalidan", password)

# Test after use function 'copy_images' and can be performed pull from new registry the specific images
def test_copy_images():
    docker_client.login("ygalidan", password)
    pull = docker_client.images.pull("ygalidan/test1", "3.8-slim-bullseye")
    assert pull is not None