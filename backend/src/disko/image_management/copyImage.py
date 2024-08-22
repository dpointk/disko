from flask import Blueprint, jsonify, request
from src.disko.image_management.image_controller import ImageController 
import os 

base_dir = os.path.dirname(os.path.abspath(__file__))
copyimage_bp = Blueprint('copyimage_bp', __name__, url_prefix='/api')

@copyimage_bp.route('/copyimage', methods=['GET'])
def copy_images():
    registry=request.args.get('new_registry')
    tag=request.args.get('tag')
    username=request.args.get('target_username')
    password=request.args.get('target_password')
    images = request.args.getlist('images')

    
    db_name = os.path.join(base_dir, '../../../image_data.db')
    controller=ImageController(db_name)
    try:
        controller.copy_images(images,registry,tag,username,password)
        return jsonify({'message': 'Images copied successfully!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
 