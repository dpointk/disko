from src.disko.image_collector import ImageCollector

if __name__ == "__main__":
    cluster = input("Enter the name of the cluster: ")
    # Print the the images collected from the Kubernetes cluster
    print(ImageCollector().collect_images(cluster))