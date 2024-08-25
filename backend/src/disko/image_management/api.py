import os
import logging
import traceback

from flask import Flask, jsonify, request
from src.disko.image_collector import ImageCollector
from src.disko.image_management.image_controller import ImageController
from src.disko.sqlite import SQLiteCRUD

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
base_dir = os.path.dirname(os.path.abspath(__file__))

def get_image_controller():
    db_name = os.path.join(base_dir, '../../../image_data.db')
    return ImageController(db_name)

@app.route('/api/clusters', methods=['GET'])
def get_clusters():
    image_controller = get_image_controller()
    clusters = image_controller.get_kubernetes_clusters()
    return jsonify(clusters)

@app.route('/api/selected-cluster', methods=['POST'])
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

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    cluster = request.args.get('cluster')
    
    if not cluster:
        return jsonify({'error': 'No cluster provided'}), 400
    
    try:
        controller = get_image_controller()
        percentages = controller.calculate_percentages(cluster)
        results = [{'registry': item[0], 'amount': item[1], 'percentage': item[2]} for item in percentages]
        return jsonify({'results': results}), 200
    except Exception as e:
        logging.error("Error in get_statistics: %s", traceback.format_exc())
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/clustermigration', methods=['GET'])
def migration():
    controller = get_image_controller()
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

@app.route('/api/images/<cluster>', methods=['GET'])
def get_images(cluster):
    try:
        db_name = os.path.join(base_dir, '../../../image_data.db')
        db = SQLiteCRUD(db_name)
        images = db.select_all(cluster)
        return jsonify(images), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
