from src.disko.image_management.image_controller import *
from src.disko.image_collector import *
from src.disko.sqlite import *

# Create db from cluster
create_db = ImageCollector().collect_images("kind-cluster1")

# Import sqlite.py to use any function on my db file
sql = SQLiteCRUD("image_data.db")

# Import image_controller.py to use any function on my db file
ctl1 = ImageController("image_data.db")

# Tesing the registry of the image
def test_calculate_amount_per_registry():
    images = sql.select_all("kind-cluster1")
    output = ctl1.calculate_amount_per_registry(images)
    for key in output.keys():
        if not isinstance(key, str): assert False
    
    for value in output.values():
        if not isinstance(value, int): assert False
    assert True

# Testing the calculation of the percentages of the images
def test_calculate_percentages():
    output = ctl1.calculate_percentages("kind-cluster1")
    for item in output:
        if not isinstance(item[0], str): assert False
        if not isinstance(item[1], int): assert False
        if not isinstance(item[2], float): assert False
    assert True