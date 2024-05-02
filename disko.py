from src.disko.image_management.image_view import ImageRegistryManager

# main function
def main():
    # Database file path
    db_file = 'image_data.db'

    # Initialize controller and GUI objects
    gui = ImageRegistryManager(db_file)
    # Set the controller object in the GUI
    gui.run()

# Entry point of the application
if __name__ == '__main__':
    main()
