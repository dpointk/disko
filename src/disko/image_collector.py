from datetime import datetime
from kubernetes import client, config
from src.disko.sqlite import SQLiteCRUD
from src.disko.image_management.image_controller import ImageController

# Class to collect images from the Kubernetes cluster
class ImageCollector:
    def __init__(self):
        self.count = 0
        self.dbfilename = "image_data.db"
        self.crud = SQLiteCRUD(self.dbfilename)
        self.controller = ImageController(self.dbfilename)

    # Initialize the database
    def initialize_db(self, db_name):
        self.crud.create_table(db_name, ["image TEXT", "timestamp TIMESTAMP", "registry TEXT"], "image, timestamp, registry")

    # Collect images from the Kubernetes cluster
    def collect_images(self, cluster):
            # initialize the database
            self.initialize_db(cluster)
            # Load the cluster configuration
            config.load_kube_config(context=cluster)
            # Create the Kubernetes API client
            v1 = client.CoreV1Api()

            print(f"Collecting images from the {cluster} cluster...")

            # Get the list of namespaces
            namespaces = [ns.metadata.name for ns in v1.list_namespace().items]

            # Dictionary to store the count of images per registry
            registry_count = {}

            # Iterate through the namespaces
            for ns in namespaces:
                # Get the list of pods in the namespace
                pods = v1.list_namespaced_pod(namespace=ns).items

                # Iterate through the pods
                for pod in pods:
                    # Iterate through containers in the pod
                    for container in pod.spec.containers:
                        image = container.image

                        # Check if the image is from Dockerhub
                        if self.controller.is_from_dockerhub(image):
                            registry = 'Dockerhub'
                        else:
                            registry = image.split('/')[0]

                        # Insert or update the image information into the SQLite database
                        scan_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        existing_image = self.crud.select_where(cluster, "image", image)
                        if existing_image:
                            # Update the existing image with the new timestamp
                            self.crud.update_data(cluster, "timestamp", scan_timestamp, "image", image)
                        else:
                            # Insert a new entry for the image
                            self.crud.insert_or_ignore_data(cluster, (image, scan_timestamp, registry))

                        # Insert or update the registry information into the SQLite database
                        existing_registry = self.crud.select_where(cluster, "registry", registry)
                        if existing_registry:
                            # Update the existing registry with the new timestamp
                            self.crud.update_data(cluster, "timestamp", scan_timestamp, "registry", registry)
                        else:
                            # Insert a new entry for the registry
                            self.crud.insert_or_ignore_data(cluster, (registry, scan_timestamp, registry_count[registry]))

            # Print the collected images
            print("\nFinished. Here are the results:")

            # Retrieve all data from the images table
            image_entries = self.crud.select_all(cluster)

            # Print image entries
            for image_data in image_entries:
                print(f"Timestamp: {image_data[1]}, Registry: {image_data[2]}, Image: {image_data[0]}")
