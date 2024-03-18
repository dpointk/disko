# main.py
from src.mvc.model import ImageDataModel 
from src.mvc.controller import ImageController
from src.disko.image_collector import ImageCollector
from src.mvc.view import ImageRegistryManager

# main function
def main():
    # set the database file
    db_file = 'image_data.db'
    # create the model and controller
    model = ImageDataModel(db_file)
    controller = ImageController(db_file)
    collector = ImageCollector()

    # get the cluster names
    cluster_names = controller.get_kubernetes_clusters()
    cluster = input("Enter the name of the cluster: \n" + str(cluster_names) + "\n")
    # initialize the database
    collector.initialize_db(cluster)
    print(ImageCollector().collect_images(cluster))

    # # insert the images with amount
    # model.insert_images_with_amount(cluster)

    # create the gui
    gui = ImageRegistryManager(db_file)
    gui.run()

if __name__ == '__main__':
    main()