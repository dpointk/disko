import docker
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
        if '.' not in parts[0] and ':' not in parts[0]:
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
        new_image_tag = f"{new_registry}:{tag}"
        pulled_image.tag(new_image_tag)

        # Push the tagged image to the new registry
        push = self.docker_client.images.push(new_image_tag)
        if push:
            print(f"Image {image} pushed to {new_registry}")
        else:
            print(f"Failed to push image {image} to {new_registry}")

    # Function for copying images to a new registry
    def copy_images(self, images, new_registry, username, password):
        count = 0
        for image in images:
            count += 1
            self.transfer_image(image, new_registry, count, username, password)

    

