from flask import Blueprint, jsonify, request ,current_app
from src.disko.image_management.image_controller import ImageController
from src.disko.sqlite import SQLiteCRUD  
import os 

base_dir = os.path.dirname(os.path.abspath(__file__))
migration_bp = Blueprint('migration_bp', __name__, url_prefix='/api')

@migration_bp.route('/clustermigration',methods=['GET'])
def migration():
    db_name = os.path.join(base_dir, '../../../image_data.db')
    controller=ImageController(db_name)

    registry=request.args.get('registry')
    tag=request.args.get('tag')
    username=request.args.get('username')
    password=request.args.get('password')
    helm_chart_path=request.args.get('helm_chart_path')

    try:
        controller.cluster_migration(registry,tag,username,password,helm_chart_path)
        return jsonify({'message': 'Image name replaced successfully in '+ helm_chart_path}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500