import traceback
from flask import Blueprint, jsonify, request
from src.disko.image_collector import ImageCollector
from src.disko.image_management.image_controller import ImageController
from src.disko.sqlite import SQLiteCRUD  
import os 
import logging

logging.basicConfig(level=logging.DEBUG)

# Create Flask Blueprints for POST and GET routes
postReq_bp = Blueprint('postReq_bp', __name__, url_prefix='/api')
getStatRes_bp = Blueprint('getStatRes', __name__, url_prefix='/api')

base_dir = os.path.dirname(os.path.abspath(__file__))

@postReq_bp.route('/selected-cluster', methods=['POST'])
def select_cluster():

    data = request.json # Parse JSON data from the incoming POST request
    cluster = data.get('cluster') # Extract 'cluster' parameter from the request data
    
    # Return a 400 error if no cluster is selected
    if not cluster:
        return jsonify({'error': 'No cluster selected'}), 400
    
    try:
        #Call the the ImageCollertor and use the collect_images function to gather data about the chosen cluster
        collector = ImageCollector()
        collector.collect_images(cluster)

        # Return a success message in JSON format if the operation was successful (200) or not (500)
        return jsonify({'message': f'Cluster {cluster} selected and processed successfully'}), 200
    except Exception as e:
        logging.error("Error in select_cluster: %s", traceback.format_exc())
        return jsonify({'error': str(e)}), 500
    

@getStatRes_bp.route('/statistics', methods=['GET'])
def get_statistics():

    cluster = request.args.get('cluster') # Get 'cluster' parameter from the query string
    
    if not cluster:
        return jsonify({'error': 'No cluster provided'}), 400 # Return a 400 error if no cluster is provided
    
    try:

        # Creating a database file path 
        db_name = os.path.join(base_dir, '../../../image_data.db')

        # Initialize the ImageController with the path to the database
        controller = ImageController(db_name)
        percentages = controller.calculate_percentages(cluster)

        # A for loop created to return to the client using a GET request
        results = []
        for item in percentages:
            results.append({
                "registry": item[0],
                "amount": item[1],
                "percentage": item[2]
            })

         # Return a success message in JSON format if the operation was successful (200) or not (500)    
        return jsonify({'results': results}), 200
    except Exception as e:
        logging.error("Error in get_statistics: %s", traceback.format_exc())
        return jsonify({'error': 'Internal Server Error'}), 500