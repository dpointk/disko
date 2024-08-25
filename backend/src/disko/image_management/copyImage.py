from flask import Blueprint, jsonify, request
from src.disko.image_management.image_controller import ImageController 
import os 

#API created to call the copy_images function to copy image from one registrey to another


base_dir = os.path.dirname(os.path.abspath(__file__))

copyimage_bp = Blueprint('copyimage_bp', __name__, url_prefix='/api')

@copyimage_bp.route('/copyimage', methods=['GET'])
def copy_images():

    # Extract query parameters from the incoming GET request
    registry=request.args.get('new_registry')
    tag=request.args.get('tag')
    username=request.args.get('target_username')
    password=request.args.get('target_password')
    images = request.args.getlist('images')

    # Creating a database file path relative to the base directory
    db_name = os.path.join(base_dir, '../../../image_data.db')

     # Initialize the ImageController with the path to the database
    controller=ImageController(db_name)
    try:

        # Call the copy_images method
        controller.copy_images(images,registry,tag,username,password)

          # Return a success message in JSON format if the operation was successful (200) or not (500)
        return jsonify({'message': 'Images copied successfully!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
 