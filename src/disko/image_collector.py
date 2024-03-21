from datetime import datetime
from kubernetes import client, config
from src.disko.sqlite import SQLiteCRUD

class ImageCollector:
    def __init__(self):
        self.count = 0
        self.dbfilename = "image_data.db"

        # Load the cluster configuration
        config.load_kube_config()

        # Create a connection to the SQLite database
        self.crud = SQLiteCRUD(self.dbfilename)
        # Create the images table if it does not exist
        self.crud.create_table("images", ["cluster_name TEXT, image_name TEXT", "timestamp TIMESTAMP, registry TEXT, amount INTEGER"], "cluster_name, image_name, timestamp")

        # Create the Kubernetes API client
        self.v1 = client.CoreV1Api()

    def collect_images(self):
        # Get the list of namespaces
        namespaces = [ns.metadata.name for ns in self.v1.list_namespace().items]

        # Iterate through the namespaces
        for ns in namespaces:
            # Get the list of pods in the namespace
            pods = self.v1.list_namespaced_pod(namespace=ns).items
            # Iterate through the pods
            for pod in pods:
                # Get the image for the pod and write it to the file
                image = pod.spec.containers[0].image
                
                # Insert the image information into the SQLite database
                scan_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # crud.insert_data("images", (image, "2022-01-01 00:00:00"))
                self.crud.insert_or_ignore_data("images", ("", image, scan_timestamp, "", 1))

                # Increase the count and print the progress message
                self.count += 1
                print(f"Scan: {scan_timestamp} Collecting... {self.count} images", end="\r")

        print(f"\nFinished. Here are the results:")
        
        # retrieve all data from the images table
        for cluster_name, image, timestamp, registry, amount in self.crud.select_all("images"):
            print(f"cluster name: {cluster_name} timestamp: {timestamp}: image: {image} registry: {registry} amount: {amount}", end="\n")
