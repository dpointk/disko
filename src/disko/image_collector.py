from datetime import datetime
from kubernetes import client, config
from src.disko.sqlite import SQLiteCRUD

# Class to collect images from the Kubernetes cluster
class ImageCollector:
    def __init__(self):
        self.count = 0
        self.dbfilename = "image_data.db"

        # Create a connection to the SQLite database
        # self.conn = sqlite3.connect("image_data.db")
        # self.cursor = self.conn.cursor()
        # self.cursor.execute("""CREATE TABLE IF NOT EXISTS images (image_name TEXT)""")
        
        self.crud = SQLiteCRUD(self.dbfilename)
        self.crud.create_table("images", ["image_name TEXT", "timestamp TIMESTAMP"], "image_name, timestamp")
        self.crud.create_table("registries", ["registry_name TEXT", "number_of_images INTEGER", "percentage TEXT"], "registry_name, number_of_images, percentage")
        self.crud.create_table("clusters", ["cluster TEXT"], "cluster")

    def collect_images(self, cluster):
        # Load the cluster configuration
        config.load_kube_config(context=cluster)
        # Create the Kubernetes API client
        v1 = client.CoreV1Api()

        print(f"Collecting images from the {cluster} cluster...")

        # Get the list of namespaces
        namespaces = [ns.metadata.name for ns in v1.list_namespace().items]

        # Open the file in write mode and clear its contents
        # with open(self.filename, "w") as f:
        #     f.truncate(0)

        # Iterate through the namespaces
        for ns in namespaces:
            # Get the list of pods in the namespace
            pods = v1.list_namespaced_pod(namespace=ns).items

            # Iterate through the pods
            for pod in pods:
                # Get the image for the pod and write it to the file
                image = pod.spec.containers[0].image
                # with open(self.filename, "a") as f:
                    # f.write(image + "\n")

                # Insert the image information into the SQLite database
                # self.cursor.execute("INSERT INTO images VALUES (?)", (image,))
                # self.conn.commit()
                scan_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # crud.insert_data("images", (image, "2022-01-01 00:00:00"))
                self.crud.insert_or_ignore_data("images", (image, scan_timestamp))

                # Increase the count and print the progress message
                self.count += 1
                print(f"Scan: {scan_timestamp} Collecting... {self.count} images", end="\r")

        print(f"\nFinished. Here are the results:")
        
        # retrieve all data from the images table
        for image,timestamp in self.crud.select_all("images"):
            print(f"timestamp: {timestamp}: image: {image}", end="\n")