from src.disko.image_management.image_controller import ImageController

# main function
def main():
    # Database file path
    db_file = 'image_data.db'

    # Run GUI
    gui = ImageController(db_file)
    gui.run_gui()

# Entry point of the application
if __name__ == '__main__':
    main()
