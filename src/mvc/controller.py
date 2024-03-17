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
        
    # check if the image is from dockerhub
    def is_from_dockerhub(self, image):
        parts = image.split('/')
        if len(parts) == 1:
            return True
        if '.' not in parts[0] and ':' not in parts[0]:
            return True
        if 'docker.io' in parts[0]:
            return True
        return False

    # calculate the amount of images per registry
    def calculate_amount_per_registry(self, images):
        amount = {}
        for image_tuple in images:
            image = image_tuple[0]
            parts = image.split('/')
            registry = parts[0]
            if self.is_from_dockerhub(image):
                registry = 'Dockerhub'
            if registry in amount:
                amount[registry] += 1
            else:
                amount[registry] = 1
        return amount
    
    # calculate the percentages of the images
    def calculate_percentages(self):
        image_data = self.db.select_all("registries")
        total_images = sum(image[0] for image in self.db.select_column('registries', 'number_of_images'))
        percentages = [(image[0], image[1], (image[1] / total_images) * 100) for image in image_data]
        return percentages
