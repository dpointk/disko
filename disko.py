from src.mvc.view import ImageRegistryManager

# main function
def main():
    # Database file path
    db_file = 'image_data.db'

    # Run GUI
    gui = ImageRegistryManager(db_file)
    gui.run()

# Entry point of the application
if __name__ == '__main__':
    main()
