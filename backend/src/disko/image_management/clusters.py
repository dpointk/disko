from flask import Blueprint, jsonify
from src.disko.image_management.image_controller import ImageController

# API created to call the copy_images function to present all local clusters on a machine

cluster_bp = Blueprint('cluster', __name__)

@cluster_bp.route('/api/clusters', methods=['GET'])
def get_clusters():

     # Initialize the ImageController with the path to the database
    image_controller = ImageController(db_file="src/disko/sqlite.py")

    # Call the get_kubernetes_clusters function
    clusters = image_controller.get_kubernetes_clusters()
    return jsonify(clusters)
