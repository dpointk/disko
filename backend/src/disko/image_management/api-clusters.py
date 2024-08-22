from flask import Blueprint, jsonify
from src.disko.image_management.image_controller import ImageController

# Create a Blueprint for cluster-related routes
cluster_bp = Blueprint('cluster', __name__)

@cluster_bp.route('/api/clusters', methods=['GET'])
def get_clusters():
    image_controller = ImageController(db_file="src/disko/sqlite.py")
    clusters = image_controller.get_kubernetes_clusters()
    return jsonify(clusters)
