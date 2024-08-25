import os
import logging
import traceback

from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS

from src.disko.image_collector import ImageCollector
from src.disko.image_management.image_controller import ImageController

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))

api = Blueprint('api', __name__, url_prefix='/api')


def get_image_controller():
    # Initializes and returns an ImageController instance connected to the database
    db_name = os.path.join(base_dir, 'image_data.db')
    print(db_name)
    return ImageController(db_name)

controller = get_image_controller()

@api.route('/clusters', methods=['GET'])
def get_clusters():
    # Fetches a list of Kubernetes clusters and returns it as a JSON response
    clusters = controller.get_kubernetes_clusters()
    return jsonify(clusters)

@api.route('/selected-cluster', methods=['POST'])
def select_cluster():
    # Processes the selected cluster by collecting images for it
    data = request.json
    cluster = data.get('cluster')
    
    if not cluster:
        return jsonify({'error': 'No cluster selected'}), 400
    
    try:
        collector = ImageCollector()
        collector.collect_images(cluster)
        return jsonify({'message': f'Cluster {cluster} selected and processed successfully'}), 200
    except Exception as e:
        logging.error("Error in select_cluster: %s", traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@api.route('/statistics', methods=['GET'])
def get_statistics():
    # Retrieves statistical data for a specified cluster and returns it as a JSON response
    cluster = request.args.get('cluster')
    
    if not cluster:
        return jsonify({'error': 'No cluster provided'}), 400
    
    try:
        percentages = controller.calculate_percentages(cluster)
        results = []
        for item in percentages:
            results.append({
                "registry": item[0],
                "amount": item[1],
                "percentage": item[2]
            })

        return jsonify({'results': results}), 200
    except Exception as e:
        logging.error("Error in get_statistics: %s", traceback.format_exc())
        return jsonify({'error': 'Internal Server Error'}), 500

@api.route('/clustermigration',methods=['GET'])
def migration():
    # Migrates a cluster's images to a new registry based on provided parameters
    registry = request.args.get('registry')
    tag = request.args.get('tag')
    username = request.args.get('username')
    password = request.args.get('password')
    helm_chart_path = request.args.get('helm_chart_path')
    
    try:
        controller.cluster_migration(registry, tag, username, password, helm_chart_path)
        return jsonify({'message': 'Image name replaced successfully in ' + helm_chart_path}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@api.route('/images/<cluster>', methods=['GET'])
def get_images(cluster):
    # Fetches the list of images associated with a given cluster and returns it as a JSON response
    try:
        images = controller.present_images_per_cluster(cluster)
        return jsonify(images), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/copyimage', methods=['GET'])
def copy_images():
    # Copies images to a new registry based on provided parameters
    registry = request.args.get('new_registry')
    tag = request.args.get('tag')
    username = request.args.get('target_username')
    password = request.args.get('target_password')
    images = request.args.getlist('images')
    
    try:
        # Call the copy_images method
        controller.copy_images(images, registry, tag, username, password)

        # Return a success message in JSON format if the operation was successful (200)
        return jsonify({'message': 'Images copied successfully!'}), 200
    except Exception as e:
        # Return an error message in JSON format if the operation failed (500)
        return jsonify({'message': str(e)}), 500
 

if __name__ == '__main__':
    # Configure the Flask app and enable CORS for the API
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.register_blueprint(api)
    app.run(debug=True)
