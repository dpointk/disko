# model.py
from src.disko.sqlite import SQLiteCRUD
from src.mvc.controller import ImageController

class ImageDataModel:
    def __init__(self, db_file):
        self.db = SQLiteCRUD(db_file)
        self.controller = ImageController(db_file)
