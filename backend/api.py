import sys
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
    db_name = os.path.join(base_dir, 'image_data.db')
    print(db_name)
    return ImageController(db_name)

controller =  get_image_controller()

@api.route('/clusters', methods=['GET'])
def get_clusters():
    clusters = controller.get_kubernetes_clusters()
    return jsonify(clusters)

@api.route('/selected-cluster', methods=['POST'])
def select_cluster():
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
    try:
        images = controller.present_images_per_cluster(cluster)
        return jsonify(images), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/copyimage', methods=['GET'])
def copy_images():

    # Extract query parameters from the incoming GET request
    registry=request.args.get('new_registry')
    tag=request.args.get('tag')
    username=request.args.get('target_username')
    password=request.args.get('target_password')
    images = request.args.getlist('images')

    # Creating a database file path relative to the base directory
    db_name = os.path.join(base_dir, 'image_data.db')

     # Initialize the ImageController with the path to the database
    controller=ImageController(db_name)
    try:

        # Call the copy_images method
        controller.copy_images(images,registry,tag,username,password)

          # Return a success message in JSON format if the operation was successful (200) or not (500)
        return jsonify({'message': 'Images copied successfully!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
 

if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.register_blueprint(api)
    app.run(debug=True)
