from src.disko.image_management.image_controller import ImageController

controller = ImageController('')
image= ["python:3.8-slim-bullseye"]

controller.copy_images(image,"diskoproject/repo_1.0","3.8-slim-bullseye","diskoproject","barbar13241324")
