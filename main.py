# main.py
from src.mvc.model import ImageDataModel
from src.mvc.controller import ImageDataController
import tkinter as tk
from tkinter import ttk
from src.disko.image_collector import ImageCollector
from src.disko.sqlite import SQLiteCRUD


def main():
    db_file = 'image_data.db'
    # Creating a connection to the database

    db = SQLiteCRUD('image_data.db')

    cluster = input("Enter the name of the cluster: ")
    # Print the the images collected from the Kubernetes cluster
    print(ImageCollector().collect_images(cluster))
    # Initialize Model, View, and Controller

    # Insert cluster names into the database
    insert_cluster_names_to_db()
    print("Clusters are successfully saved in the database.")


    model = ImageDataModel(db_file)
    controller = ImageDataController(model)
    # Creating the table for the registries
    controller.process_image_data()

    # Create the main window and run the GUI application
    root = tk.Tk()
    root.title("Image Registry Manager")
    root.style = ttk.Style()
    root.style.theme_use('clam')

    columns = ['Registry Name', 'Number of images', 'Percentage']
    view = ImagesTableView(root, columns)
    root.mainloop()

if __name__ == '__main__':
    main()
