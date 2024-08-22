from flask import Blueprint, jsonify, request
from src.disko.sqlite import SQLiteCRUD  
import os 

base_dir = os.path.dirname(os.path.abspath(__file__))
imageShow_bp = Blueprint('imageShow_bp', __name__, url_prefix='/api')

@imageShow_bp.route('/images/<cluster>', methods=['GET'])
def get_images(cluster):
    try:
        db_name = os.path.join(base_dir, '../../../image_data.db')
        
       
    
        db = SQLiteCRUD(db_name)
        table_name=cluster
        images = db.select_all(table_name)
        
        
        return jsonify(images), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

