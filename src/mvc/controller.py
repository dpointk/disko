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
        ammount = {}
        for image_tuple in images:
            image = image_tuple[0]
            parts = image.split('/')
            registry = parts[0]
            if self.is_from_dockerhub(image):
                if 'Dockerhub' in ammount:
                    ammount['Dockerhub'] += 1
                else:
                    ammount['Dockerhub'] = 1
            elif registry in ammount:
                ammount[registry] += 1
            else:
                ammount[registry] = 1
        return ammount


    
    # calculate the percentages of the images
    def calculate_percentages(self, db_name):
        image_data = self.crud.select_all(db_name)
        total_images = sum(image[3] for image in image_data)  # 'number_of_images' is the 4th column
        percentages = [(image[0], image[3], (image[3] / total_images) * 100) for image in image_data]
        return percentages
