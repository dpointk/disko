from flask import Blueprint, jsonify, request ,current_app
from src.disko.image_management.image_controller import ImageController
from src.disko.sqlite import SQLiteCRUD  
import os 

#API created to implement the cluster_migration function to the frontend, transfering an image from one registry to another using helm


base_dir = os.path.dirname(os.path.abspath(__file__))
migration_bp = Blueprint('migration_bp', __name__, url_prefix='/api')

@migration_bp.route('/clustermigration',methods=['GET'])
def migration():

    # Creating a database file path relative to the base directory
    db_name = os.path.join(base_dir, '../../../image_data.db')

    # Initialize the ImageController with the path to the database
    controller=ImageController(db_name)

    # Extract query parameters from the incoming GET request
    registry=request.args.get('registry')
    tag=request.args.get('tag')
    username=request.args.get('username')
    password=request.args.get('password')
    helm_chart_path=request.args.get('helm_chart_path')
 
    try:

        # Call the cluster_migration method
        controller.cluster_migration(registry,tag,username,password,helm_chart_path)

        # Return a success message in JSON format if the operation was successful (200) or not (500)
        return jsonify({'message': 'Image name replaced successfully in '+ helm_chart_path}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500