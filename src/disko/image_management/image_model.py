# model.py
from src.disko.sqlite import SQLiteCRUD

class ImageDataModel:
    def __init__(self, db_file):
        self.db = SQLiteCRUD(db_file)
