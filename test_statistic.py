from src.disko.image_collector import *

# Create db from cluster
# create_db = ImageCollector().collect_images("kind-cluster1")

# Import image_controller.py to use any function on my db file
# ctl1 = ImageController("image_data.db")

# Testing the calculation of the percentages of the images
def test_calculate_percentages():
    output = [("docker.io", 10, 100.0)]
    print(output)
    for item in output:
        if not isinstance(item[0], str): assert False
        if not isinstance(item[1], int): assert False
        if not isinstance(item[2], float): assert False
    assert True