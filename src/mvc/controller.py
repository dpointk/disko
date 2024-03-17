from src.disko.sqlite import SQLiteCRUD
from kubernetes import config

# controller.py
class imageController:
    def __init__(self, model):
        self.model = model

    def process_image_data(self):
        self.model.insert_images_with_amount()
        print("Registries are successfully saved in the database.")

    # Checking if the image is from Dockerhub
def is_from_dockerhub(image):
    parts = image.split('/')
    if len(parts) == 1:
        return True
    if '.' not in parts[0] and ':' not in parts[0]:
        return True
    if 'docker.io' in parts[0]:
        return True
    return False

# Getting the registry of the image
def calculate_amount_per_registry(images):
    amount = {}
    for image_tuple in images:
        image = image_tuple[0]
        parts = image.split('/')
        registry = parts[0]
        if is_from_dockerhub(image):
            if 'Dockerhub' in amount:
                amount['Dockerhub'] += 1
            else:
                amount['Dockerhub'] = 1
        elif registry in amount:
            amount[registry] += 1
        else:
            amount[registry] = 1
    return amount

def get_kubernetes_clusters():
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