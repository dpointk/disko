import ruamel.yaml
import subprocess
import yaml
import docker
import hashlib
import os
from src.disko.sqlite import SQLiteCRUD
from kubernetes import config


# controller.py
class ImageController:
    def __init__(self, db_file):
        self.db = SQLiteCRUD(db_file)
        self.docker_client = docker.from_env()

    # get the kubernetes clusters
    def get_kubernetes_clusters(self):
        try:
            # Load kubeconfig file
            config.load_kube_config()

            # Get contexts from kubeconfig
            contexts, _ = config.list_kube_config_contexts()

            # Extract cluster names
            cluster_names = [context["context"]["cluster"] for context in contexts]

            return cluster_names

        except Exception as e:
            print("Error:", e)
            return []   
        
    # Checking if the image is from Dockerhub
    def is_from_dockerhub(self, image):
        parts = image.split('/')
        if len(parts) == 1:
            return True
        if '.' not in parts[0]:
            return True
        if 'docker.io' in parts[0]:
            return True
        return False

    # Getting the registry of the image
    def calculate_amount_per_registry(self, images):
        amount = {}
        for image_tuple in images:
            registry = image_tuple[2]  # Index 2 corresponds to the registry in the image_data tuple
            amount[registry] = amount.get(registry, 0) + 1  # Increment the count for the registry
        return amount


    # calculate the percentages of the images
    def calculate_percentages(self, table_name):
        image_data = self.db.select_all(table_name)
        amounts = self.calculate_amount_per_registry(image_data)
        total_images = sum(amounts.values())
        percentages = [(registry, amount, (amount / total_images) * 100) for registry, amount in amounts.items()]
        return percentages
            

    # Function for pulling and pushing an image to a new registry
    def transfer_image(self, image, new_registry, tag, username, password):
        # Docker login
        self.docker_client.login(username=username, password=password)

        # Pull the image
        pulled_image = self.docker_client.images.pull(image)
        if pulled_image:
            print(f"Image {image} pulled successfully")

        # Tag the pulled image with new registry
        new_image_tag = f"{new_registry}:{tag}".strip()
        pulled_image.tag(new_image_tag)

        # Push the tagged image to the new registry
        push = self.docker_client.images.push(new_image_tag)
        if push:
            print(f"Image {image} pushed to {new_registry}")
        else:
            print(f"Failed to push image {image} to {new_registry}")


    def copy_images(self, images, new_registry, tag, username, password):
        for image in images:
            # Check if image is a tuple
            if isinstance(image, tuple):
                image_name = image[0]
            else:
                image_name = image

            # Check if image_name contains a tag
            if ":" in image_name:
                image_name, image_tag = image_name.split(":")
            else:
                image_tag = tag

            self.transfer_image(image_name, new_registry, tag, username, password)
            self.export_sha256(image_name, image_tag)

    def export_sha256(self, image_name, image_tag):
        sha256_hash = hashlib.sha256(f"{image_name}:{image_tag}".encode()).hexdigest()
        with open("sha256_hashes.txt", "a") as file:
            file.write(f"{image_name}:{image_tag} - SHA256: {sha256_hash}\n")

    # Function for replacing an image in .values file
    def replace_image(self, values_file_path, new_image):
        yaml = ruamel.yaml.YAML()
        yaml.indent(mapping=2, sequence=4, offset=2)
                                
        # Read the contents of the .values file
        try:
            with open(values_file_path, 'r') as file:
                data = yaml.load(file)
        except FileNotFoundError:
            print(f"Error: File '{values_file_path}' not found.")
            return

        # Update the image name value
        if 'image' in data:
            data['image'] = new_image
        else:
            print("Error: Could not find 'image' in the YAML file.")
            return

        # Write the modified contents back to the file
        try:
            with open(values_file_path, 'w') as file:
                yaml.dump(data, file)
            print(f"Image name replaced successfully in '{values_file_path}'.")
        except Exception as e:
            print(f"Error occurred while writing to '{values_file_path}': {e}")

    # Function for getting the current image name from a .values file
    def get_current_image(self, values_file_path):
        yaml = ruamel.yaml.YAML(typ='safe', pure=True)
        
        # Read the contents of the .values file
        try:
            with open(values_file_path, 'r') as file:
                data = yaml.load(file)
        except FileNotFoundError:
            print(f"Error: File '{values_file_path}' not found.")
            return None

        # Extract the current image name
        if 'image' in data:
            current_image_name = data['image']
            print(f"Current image name in '{values_file_path}': {current_image_name}")
            return [current_image_name]
        else:
            print("Error: Could not find 'image' in the YAML file.")
            return None
        
    
    # Function for getting the release name from a Chart.yaml file
    def get_release_name(self, chart_file_path):
        # Read the contents of the Chart.yaml file
        try:
            with open(chart_file_path, 'r') as file:
                data = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Error: File '{chart_file_path}' not found.")
            return None

        # Extract the release name
        if 'name' in data:
            release_name = data['name']
            print(f"Release name: {release_name}")
            return release_name
        else:
            print("Error: Could not find 'name' in the Chart.yaml file.")
            return None


    # Function for upgrading a Helm release
    def helm_upgrade_release(self, release_name, chart_path):
        try:
            # Run the helm upgrade command
            subprocess.run(
                ["helm", "upgrade", release_name, chart_path],
                check=True
            )
            print(f"Helm upgrade for release '{release_name}' successful.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred during helm upgrade: {e}")


    # Function for Kubernetes cluster migration
    def cluster_migration(self, registry, tag, username, password, helm_chart_path):
        values_file_path = os.path.join(helm_chart_path, "values.yaml")
        chart_file_path = os.path.join(helm_chart_path, "Chart.yaml")
        release_name = self.get_release_name(chart_file_path)
        current_image = self.get_current_image(values_file_path)
        self.copy_images(current_image, registry, tag, username, password)
        self.replace_image(values_file_path, registry)
        self.helm_upgrade_release(release_name, helm_chart_path)


