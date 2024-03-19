# main.py
from src.mvc.controller import ImageController
from src.disko.image_collector import ImageCollector
from src.mvc.view import ImageRegistryManager

# main function
def main():
    db_file = 'image_data.db'
    # Declare mvc objects
    controller = ImageController(db_file)
    gui = ImageRegistryManager(db_file)
    # Get the kubernetes clusters
    cluster_names = controller.get_kubernetes_clusters()
    # Run the GUI
    gui.cluster_selection(cluster_names)
    gui.run()


if __name__ == '__main__':
    main()