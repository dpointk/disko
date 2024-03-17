from kubernetes import config
from src.disko.sqlite import SQLiteCRUD

db = SQLiteCRUD('image_data.db')

def get_kubernetes_clusters():
    try:
        # Load kubeconfig file
        config.load_kube_config()

        # Get contexts from kubeconfig
        contexts, _ = config.list_kube_config_contexts()

        # Extract cluster names
        cluster_names = [context["context"]["cluster"] for context in contexts]

        return cluster_names

    except Exception as e:
        print("Error:", e)
        return []
    
# Insert cluster names into the database
def insert_cluster_names_to_db():
    cluster_names = get_kubernetes_clusters()
    for cluster_name in cluster_names:
        db.insert_data('clusters', (cluster_name,))

if __name__ == "__main__":
    insert_cluster_names_to_db()
    print("Clusters are successfully saved in the database.")

