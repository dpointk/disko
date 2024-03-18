from datetime import datetime
from kubernetes import client, config
from src.disko.sqlite import SQLiteCRUD
from src.mvc.controller import ImageController

# Class to collect images from the Kubernetes cluster
class ImageCollector:
    def __init__(self):
        self.count = 0
        self.dbfilename = "image_data.db"
        self.crud = SQLiteCRUD(self.dbfilename)
        self.controller = ImageController(self.dbfilename)

    def initialize_db(self, db_name):
        self.crud.create_table(db_name, ["image TEXT", "timestamp TIMESTAMP", "registry TEXT", "amount INTEGER"], "image, timestamp, registry, amount")

    def collect_images(self, cluster):
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
                # Get the image for the pod
                image = pod.spec.containers[0].image

                # Check if the image is from Dockerhub
                if self.controller.is_from_dockerhub(image):
                    registry = 'Dockerhub'
                else:
                    registry = image.split('/')[0]

                # Increment the count for the registry
                registry_count[registry] = registry_count.get(registry, 0) + 1

        # Insert or update the registry information into the SQLite database
        scan_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for registry, count in registry_count.items():
            # Check if the registry already exists in the database
            existing_registry = self.crud.select_all(cluster)
            existing_registry = [entry for entry in existing_registry if entry[2] == registry]  # Index 2 corresponds to the registry column
            if existing_registry:
                # Update the existing registry with the new timestamp and count
                self.crud.update_data(cluster, "timestamp", scan_timestamp, "registry", registry)
                self.crud.update_data(cluster, "amount", count, "registry", registry)
            else:
                # Insert a new entry for the registry
                self.crud.insert_or_ignore_data(cluster, (None, scan_timestamp, registry, count))

        print(f"\nFinished. Here are the results:")

        # retrieve all data from the images table
        registry_entries = []
        image_entries = []
        for registry_data in self.crud.select_all(cluster):
            if registry_data[2] is not None:
                registry_entries.append(registry_data)
            else:
                image_entries.append(registry_data)

        # Print registry entries
        for registry_data in registry_entries:
            print(f"Timestamp: {registry_data[1]}, Registry: {registry_data[2]}, Amount: {registry_data[3]}, Image: {registry_data[0]}")

        # Print image entries
        for registry_data in image_entries:
            print(f"Timestamp: {registry_data[1]}, Registry: {registry_data[2]}, Amount: {registry_data[3]}, Image: {registry_data[0]}")
