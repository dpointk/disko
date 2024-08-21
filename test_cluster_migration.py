from src.disko.image_collector import *
import getpass
import os

path = "Octopus/Project_final/disko"
os.chdir(path)

# Create db from cluster
create_db = ImageCollector().collect_images("kind-cluster1")

# Import image_controller.py to use any function on my db file
ctl1 = ImageController("image_data.db")

password = getpass.getpass("Enter your password: ")
ctl1.cluster_migration("ygalidan/test1", "1", "ygalidan", password, "disko")