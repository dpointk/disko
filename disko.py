from src.disko.image_management.image_model import ImageDataModel
from src.disko.image_management.image_controller import ImageController

# main function
def main():
    # Database file path
    model = ImageDataModel()
    db = model.get_db()

    # Run GUI
    app = ImageController(db)
    app.run()

# Entry point of the application
if __name__ == '__main__':
    main()
