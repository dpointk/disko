from src.disko.image_management.image_controller import ImageController
import os

os.chdir("/home/gatmbarz123/Desktop/DISKO-P/disko/backend")

controller = ImageController("/home/gatmbarz123/Desktop/DISKO-P/disko/backend/image_data.db")

registry = "diskoproject/repo_1.0"
tag = "3.8-slim-bullseye" 
username = "diskoproject"
password = "barbar13241324"
helm_chart_path = "/home/gatmbarz123/Desktop/bar"

print(controller.cluster_migration(registry, tag, username, password,helm_chart_path))