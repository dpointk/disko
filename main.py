from src.mvc.controller import ImageController
from src.mvc.view import ImageRegistryManager

# main function
def main():
    # Database file path
    db_file = 'image_data.db'

    # Initialize controller and GUI objects
    controller = ImageController(db_file)
    gui = ImageRegistryManager(db_file)

    # Get the list of Kubernetes clusters
    cluster_names = controller.get_kubernetes_clusters()

    # Show cluster selection window and run GUI
    
    gui.run()
    #gui.cluster_selection(cluster_names)

# Entry point of the application
if __name__ == '__main__':
    main()
