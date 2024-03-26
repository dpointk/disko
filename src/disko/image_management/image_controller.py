from kubernetes import config
from src.disko.image_collector import ImageCollector
from tkinter import messagebox
from src.disko.image_management.image_view import ImageRegistryManager

# controller.py
class ImageController:
    def __init__(self, db):
        self.db = db  # SQLiteCRUD instance
        self.image_collector = ImageCollector()  # ImageCollector instance
        self.view = None  # ImageRegistryManager instance


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
            registry = image_tuple[3]  # Index 3 corresponds to the registry column in the db
            amount[registry] = amount.get(registry, 0) + 1  # Increment the count for the registry
        return amount
    
    def get_view(self):
        if not self.view:
            self.view = ImageRegistryManager()
            self.view.set_controller(self)
        return self.view
    
    def get_image_data(self):
        return self.db.select_all('images')
    

    def get_registry_amount(self):
        # Get the image data from the database
        image_data = self.get_image_data()
        # Calculate the number of images per registry
        registry_amount = self.calculate_amount_per_registry(image_data)

        return registry_amount
    

    def confirm_cluster_selection(self, selected_cluster, cluster_selection_window):
        self.view = self.get_view()
        # Confirm cluster selection
        if selected_cluster:
            cluster_selection_window.destroy()  # Close the cluster selection window
            self.image_collector.collect_images(selected_cluster)  # Collect images for the selected cluster
            self.selected_cluster = selected_cluster  # Update selected cluster variable
            registry_amount = self.get_registry_amount()  # Get the number of images per registry
            self.view.display_image_data(selected_cluster, registry_amount)  # Display image data for the selected cluster
        else:
            messagebox.showerror("Error", "Please select a cluster.")  # Show error message if no cluster selected

    def run(self):
        self.view = self.get_view()
        cluster_names = self.get_kubernetes_clusters()
        self.view.run_gui(cluster_names)


