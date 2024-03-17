# model.py
from src.disko.sqlite import SQLiteCRUD

class ImageDataModel:
    def __init__(self, db_file):
        self.db = SQLiteCRUD(db_file)

    def is_from_dockerhub(self, image):
        parts = image.split('/')
        if len(parts) == 1:
            return True
        if '.' not in parts[0] and ':' not in parts[0]:
            return True
        if 'docker.io' in parts[0]:
            return True
        return False

    def calculate_amount_per_registry(self):
        images = self.db.select_column('images', 'image_name')
        amount = {}
        for image in images:
            registry = image.split('/')[0]
            if self.is_from_dockerhub(image):
                registry = 'Dockerhub'
            if registry in amount:
                amount[registry] += 1
            else:
                amount[registry] = 1
        return amount

    def insert_images_with_amount(self):
        amounts = self.calculate_amount_per_registry()
        total_images = len(self.db.select_column('images', 'image_name'))
        for registry, count in amounts.items():
            percentage = (count / total_images) * 100
            self.db.insert_data('registries', (registry, count, f'{percentage:.0f}%'))

    # Inserting the registries with the amount of images
    def insert_images_with_amount(db):
        amount = calculate_amount_per_registry(db.select_column('images', 'image_name'))
        for registry, amount in amount.items():
       # precentage = (amount / len(db.select_column('images', 'image_name'))) * 100
            db.insert_data('registries', (registry, amount))
