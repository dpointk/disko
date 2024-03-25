from src.disko.sqlite import SQLiteCRUD
from kubernetes import config
import tkinter as tk
from tkinter import ttk, messagebox
from src.disko.image_management.image_view import ImageRegistryManager
from src.disko.image_collector import ImageCollector

# controller.py
class ImageController:
    def __init__(self, db_file):
        self.db = SQLiteCRUD(db_file)
        self.view = ImageRegistryManager()
        self.image_collector = ImageCollector()  # ImageCollector instance
        self.root = tk.Tk()  # Tkinter root window
        self.root.title("Image Registry Manager")  # Window title
        self.root.style = ttk.Style()  # Tkinter style
        self.root.style.theme_use('clam')  # Use 'clam' theme
        self.columns = ['Cluster Name', 'Registry Name', 'Number of Images']  # Table columns
        self.treeview = None  # Treeview widget
        # Checkbox variables for each column
        self.checkboxes = {col: tk.BooleanVar(value=True) for col in self.columns}
        self.selected_cluster = None  # Initialize selected cluster variable

    # get the kubernetes clusters
    def get_kubernetes_clusters(self):
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
        
    # Checking if the image is from Dockerhub
    def is_from_dockerhub(self, image):
        parts = image.split('/')
        if len(parts) == 1:
            return True
        if '.' not in parts[0]:
            return True
        if 'docker.io' in parts[0]:
            return True
        return False

    # Getting the registry of the image
    def calculate_amount_per_registry(self, images):
        amount = {}
        for image_tuple in images:
            registry = image_tuple[3]  # Index 3 corresponds to the registry column in the db
            amount[registry] = amount.get(registry, 0) + 1  # Increment the count for the registry
        return amount
    
    def get_image_data(self):
        return self.db.select_all('images')
    
    def cluster_selection(self, clusters, treeview):
        # Open a new window for cluster selection
        cluster_selection_window = tk.Toplevel(self.root)
        cluster_selection_window.title("Cluster Selection")
        # Lift the window above other windows
        cluster_selection_window.lift()
        # Ensure the window receives focus
        cluster_selection_window.focus_force()
        # Add label and combobox for cluster selection
        label = ttk.Label(cluster_selection_window, text="Please select a cluster:")
        label.pack()
        cluster_var = tk.StringVar()
        cluster_combobox = ttk.Combobox(cluster_selection_window, textvariable=cluster_var, values=clusters)
        cluster_combobox.pack()

        # Add confirm button to confirm cluster selection
        confirm_button = ttk.Button(cluster_selection_window, text="Confirm", command=lambda: self.confirm_cluster_selection(cluster_var.get(), cluster_selection_window, treeview))
        confirm_button.pack()

    def confirm_cluster_selection(self, selected_cluster, cluster_selection_window, treeview):
        # Confirm cluster selection
        if selected_cluster:
            cluster_selection_window.destroy()  # Close the cluster selection window
            self.image_collector.collect_images(selected_cluster)  # Collect images for the selected cluster
            self.selected_cluster = selected_cluster  # Update selected cluster variable
            registry_amount = self.get_registry_amount()  # Get the number of images per registry
            self.view.display_image_data(selected_cluster, registry_amount, treeview)  # Display image data for the selected cluster
        else:
            messagebox.showerror("Error", "Please select a cluster.")  # Show error message if no cluster selected

    def get_registry_amount(self):
        # Get the image data from the database
        image_data = self.get_image_data()
        # Calculate the number of images per registry
        registry_amount = self.calculate_amount_per_registry(image_data)

        return registry_amount

    def get_button_select_cluster(self):
        cluster_names = self.get_kubernetes_clusters()
        return ttk.Button(self.root, text="Select Cluster", command=lambda: self.cluster_selection(cluster_names), style='Custom.TButton')

    def run_gui(self):
        # Run the application
        frame = ttk.Frame(self.root, style='DarkFrame.TFrame')
        frame.pack(padx=100, pady=100)

        # Create treeview for displaying image data
        self.treeview = ttk.Treeview(frame, columns=self.columns, show='headings', style='Custom.Treeview')
        for col in self.columns:
            self.treeview.heading(col, text=col)  # Set column headings

        self.treeview.pack(side='left', fill='both', expand=True)

        # Add scrollbar to the treeview
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.treeview.yview)
        scrollbar.pack(side='right', fill='y')
        self.treeview.configure(yscrollcommand=scrollbar.set)

        cluster_names = self.get_kubernetes_clusters()

        # Add buttons for cluster selection
        button_select_cluster = ttk.Button(self.root, text="Select Cluster", command=lambda: self.cluster_selection(cluster_names, self.treeview), style='Custom.TButton')
        button_select_cluster.pack(pady=10)

        # Add buttons for displaying data, and showing images table
        button_show_images_table = ttk.Button(self.root, text="Show Images Table", command=lambda: self.view.create_images_table_screen(self.root, self.selected_cluster), style='Custom.TButton')
        button_show_images_table.pack(pady=10)
        self.root.mainloop()  # Start the main event loop

