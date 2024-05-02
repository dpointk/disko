# model.py
from src.disko.sqlite import SQLiteCRUD

class ImageDataModel:
    def __init__(self):
        self.db = SQLiteCRUD('image_data.db')
    
    def get_db(self):
        return self.db
