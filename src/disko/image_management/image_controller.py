from kubernetes import config
from src.disko.image_collector import ImageCollector
from tkinter import messagebox
from src.disko.image_management.image_view import ImageRegistryManager

# controller.py
class ImageController:
    def __init__(self, db):
        self.db = db  # SQLiteCRUD instance
        self.image_collector = ImageCollector()  # ImageCollector instance
        self.view = ImageRegistryManager()  # ImageRegistryManager instance
  
        
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
            registry = image_tuple[2]  # Index 2 corresponds to the registry column in the db
            amount[registry] = amount.get(registry, 0) + 1  # Increment the count for the registry
        return amount
    
    
    def get_image_data(self):
        return self.db.select_all('images')
    

    def get_registry_amount(self):
        # Get the image data from the database
        image_data = self.get_image_data()
        # Calculate the number of images per registry
        registry_amount = self.calculate_amount_per_registry(image_data)
        return registry_amount

        
    def run(self):
        self.image_collector.collect_images()  # Collect images for the selected cluster
        registry_amount = self.get_registry_amount()  # Get the number of images per registry
        image_data = self.get_image_data()  # Get the image data
        self.view.run_gui(registry_amount, image_data)


