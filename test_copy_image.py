from src.disko.image_collector import *
import os
import docker
docker_client = docker.from_env()

# Import image_controller.py to use any function on my db file
ctl1 = ImageController("image_data.db")
password = os.getenv("DOCKERHUB_PASSWORD")

images = ["python:3.8-slim-bullseye"]

ctl1.copy_images(images, "ygalidan/test1", "3.8-slim-bullseye", "ygalidan", password)

def test_copy_images():
    docker_client.login("ygalidan", password)
    pull = docker_client.images.pull("ygalidan/test1", "3.8-slim-bullseye")
    assert pull is not None

