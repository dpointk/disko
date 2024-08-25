from flask import Blueprint, jsonify, request
from src.disko.sqlite import SQLiteCRUD  
import os 

#API created to present the table of a specific cluster from the database
 
base_dir = os.path.dirname(os.path.abspath(__file__))
imageShow_bp = Blueprint('imageShow_bp', __name__, url_prefix='/api')


#

@imageShow_bp.route('/images/<cluster>', methods=['GET'])
def get_images(cluster):
    try:
        # Creating a database file path 
        db_name = os.path.join(base_dir, '../../../image_data.db')
        
        #Initializing the database classwith the database's path
        db = SQLiteCRUD(db_name)

        #Set the table name to the 'cluster'
        table_name=cluster

        #Retrieve all records from a certain table 
        images = db.select_all(table_name)
        
        # Return a success message in JSON format if the operation was successful (200) or not (500)
        return jsonify(images), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

