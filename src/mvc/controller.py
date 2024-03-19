from src.disko.sqlite import SQLiteCRUD
from kubernetes import config

# controller.py
class ImageController:
    def __init__(self, db_file):
        self.db = SQLiteCRUD(db_file)

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

    

