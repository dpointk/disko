import tkinter as tk
from tkinter import ttk, messagebox
from src.disko.sqlite import SQLiteCRUD
from src.mvc.controller import ImageController
from src.disko.image_collector import ImageCollector

class ImageRegistryManager:
    def __init__(self, db_file):
        # Initialize the ImageRegistryManager
        self.db = SQLiteCRUD(db_file)  # SQLite database handler
        self.root = tk.Tk()  # Tkinter root window
        self.root.title("Image Registry Manager")  # Window title
        self.root.style = ttk.Style()  # Tkinter style
        self.root.style.theme_use('clam')  # Use 'clam' theme
        self.columns = ['Registry Name', 'Number of Images', 'Percentage']  # Table columns
        self.treeview = None  # Treeview widget
        # Checkbox variables for each column
        self.checkboxes = {col: tk.BooleanVar(value=True) for col in self.columns}
        self.controller = ImageController(db_file)  # ImageController instance
        self.image_collector = ImageCollector()  # ImageCollector instance
        self.selected_cluster = None  # Initialize selected cluster variable
        self.pull_username = None
        self.pull_password = None
        self.push_username = None
        self.push_password = None
        self.listbox = None
        self.selected_images = []

    def display_image_data(self, table_name):
        # Clear existing data in the treeview
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        # Get the image data from the database
        image_data = self.db.select_all(table_name)

        # Calculate the number of images per registry
        registry_amount = self.controller.calculate_amount_per_registry(image_data)

        # Calculate the percentages of the images
        percentages = self.controller.calculate_percentages(table_name)

        # Populate the treeview with the data
        for registry, num_images in registry_amount.items():
            # Find the percentage corresponding to the registry
            percentage = next((p[2] for p in percentages if p[0] == registry), 0)
            # Insert the data into the treeview
            self.treeview.insert('', 'end', values=(registry, num_images, f"{percentage:.0f}%"))

    def cluster_selection(self, clusters):
        # Open a new window for cluster selection
        cluster_selection_window = tk.Toplevel(self.root)
        cluster_selection_window.title("Cluster Selection")

        # Add label and combobox for cluster selection
        label = ttk.Label(cluster_selection_window, text="Please select a cluster:")
        label.pack()
        cluster_var = tk.StringVar()
        cluster_combobox = ttk.Combobox(cluster_selection_window, textvariable=cluster_var, values=clusters)
        cluster_combobox.pack()

        # Add confirm button to confirm cluster selection
        confirm_button = ttk.Button(cluster_selection_window, text="Confirm", command=lambda: self.confirm_cluster_selection(cluster_var.get(), cluster_selection_window))
        confirm_button.pack()

    def confirm_cluster_selection(self, selected_cluster, cluster_selection_window):
        # Confirm cluster selection
        if selected_cluster:
            cluster_selection_window.destroy()  # Close the cluster selection window
            self.image_collector.collect_images(selected_cluster)  # Collect images for the selected cluster
            self.selected_cluster = selected_cluster  # Update selected cluster variable
            self.display_image_data(selected_cluster)  # Display image data for the selected cluster
        else:
            messagebox.showerror("Error", "Please select a cluster.")  # Show error message if no cluster selected

    def create_images_table_screen(self):
        # Create a new window for displaying images table
        images_table_window = tk.Toplevel(self.root)
        images_table_window.title("Images Table")

        # Add frame for layout
        frame = ttk.Frame(images_table_window, style='DarkFrame.TFrame')
        frame.pack(padx=20, pady=20)

        # Create treeview for displaying image data
        self.treeview = ttk.Treeview(frame, columns=['Image', 'TimeStamp'], show='headings', style='Custom.Treeview')
        self.treeview.heading('Image', text='Image')  # Set column heading for image
        self.treeview.heading('TimeStamp', text='TimeStamp')  # Set column heading for timestamp
        self.treeview.pack(side='left', fill='both', expand=True)

        # Add scrollbar to the treeview
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.treeview.yview)
        scrollbar.pack(side='right', fill='y')
        self.treeview.configure(yscrollcommand=scrollbar.set)

        # Retrieve image data for the selected cluster
        if self.selected_cluster:
            image_data = self.db.select_all(self.selected_cluster)

            # Populate the treeview with image data
            for image in image_data:
                self.treeview.insert('', 'end', values=(image[0], image[1]))  # Insert image data into the treeview
        else:
            messagebox.showerror("Error", "No cluster selected.")  # Show error message if no cluster is selected

    def update_columns(self):
        # Update column display based on checkbox selection
        selected_columns = [column.get() for column in self.checkboxes.values()]
        for col in self.columns:
            if col in selected_columns:
                self.treeview.column(col, display=True)
            else:
                self.treeview.column(col, display=False)
    
    def select_docker_images(self):
        # Get the list of image names from the database
        image_names = self.db.select_all(self.selected_cluster)  

        # Define the fixed window size
        window_width = 700
        window_height = 300

        # Open a new window for selecting images
        select_images_window = tk.Toplevel(self.root)
        select_images_window.title("Select Docker Images")
        select_images_window.geometry(f"{window_width}x{window_height}")  # Set fixed window size

        # Add label and listbox for image selection
        label = ttk.Label(select_images_window, text="Please select Docker images:")
        label.pack()

        # Determine the width of the listbox based on the length of the longest text
        max_text_width = max(len(name) for name in image_names)
        listbox_width = min(max_text_width * 10, 300)  # Set a maximum width of 300

        # Create a listbox for displaying image names
        self.listbox = tk.Listbox(select_images_window, selectmode=tk.MULTIPLE, width=listbox_width)
        for name in image_names:
            self.listbox.insert(tk.END, name)
        self.listbox.pack(expand=True, fill='both')

        # Add confirm button to confirm image selection
        confirm_button = ttk.Button(select_images_window, text="Confirm", command=lambda: self.confirm_image_selection(self.listbox.curselection(), select_images_window))
        confirm_button.pack()

    def confirm_image_selection(self, selected_indices, select_images_window):
        # Confirm image selection
        if selected_indices:
            selected_images = [self.listbox.get(index) for index in selected_indices]
            self.selected_images = [self.listbox.get(index) for index in selected_indices]  # Store selected images as a list
            select_images_window.destroy()  # Close the image selection window
            self.registry_input_screen(selected_images)  # Transition to input screen for registry details
        else:
            messagebox.showerror("Error", "Please select Docker images.")
    
    def registry_input_screen(self, selected_images):
        # Open a new window for entering registry details
        registry_input_window = tk.Toplevel(self.root)
        registry_input_window.title("Registry Input")
        
        # Add label and entry for username and password for pulling registry
        pull_label = ttk.Label(registry_input_window, text="Pulling Registry:")
        pull_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        pull_username_label = ttk.Label(registry_input_window, text="Username:")
        pull_username_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        pull_username_entry = ttk.Entry(registry_input_window)
        pull_username_entry.grid(row=1, column=1, padx=5, pady=5)
        pull_password_label = ttk.Label(registry_input_window, text="Password:")
        pull_password_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        pull_password_entry = ttk.Entry(registry_input_window, show="*")
        pull_password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Add label and entry for username and password for pushing registry
        push_url_label = ttk.Label(registry_input_window, text="Pushing Registry URL:")
        push_url_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        push_url_entry = ttk.Entry(registry_input_window)
        push_url_entry.grid(row=3, column=1, padx=5, pady=5)
        
        push_username_label = ttk.Label(registry_input_window, text="Username:")
        push_username_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        push_username_entry = ttk.Entry(registry_input_window)
        push_username_entry.grid(row=4, column=1, padx=5, pady=5)
        
        push_password_label = ttk.Label(registry_input_window, text="Password:")
        push_password_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        push_password_entry = ttk.Entry(registry_input_window, show="*")
        push_password_entry.grid(row=5, column=1, padx=5, pady=5)
        
        # Add button to submit registry details
        submit_button = ttk.Button(registry_input_window, text="Submit", command=lambda: self.submit_registry_details(
            pull_username_entry.get(), pull_password_entry.get(), push_username_entry.get(), push_password_entry.get(),
            push_url_entry.get(), registry_input_window))
        submit_button.grid(row=6, column=0, columnspan=2, pady=10)


    def submit_registry_details(self, pull_username, pull_password, push_username, push_password, push_url, window):
        # Handle submission of registry details
        self.pull_username = pull_username
        self.pull_password = pull_password
        self.push_username = push_username
        self.push_password = push_password
        self.push_url = push_url  # Store the push URL
        
        # Perform actions with the entered registry details
        
        # Close the input window
        window.destroy()


    def run(self):
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

        cluster_names = self.controller.get_kubernetes_clusters()

        # Add buttons for cluster selection, displaying data, and showing images table
        button_select_cluster = ttk.Button(self.root, text="Select Cluster", command=lambda: self.cluster_selection(cluster_names), style='Custom.TButton')
        button_select_cluster.pack(pady=10)
        
        button_change_registry = ttk.Button(self.root, text="Change Registry", command=self.select_docker_images, style='Custom.TButton')
        button_change_registry.pack(pady=10)

        button_show_images_table = ttk.Button(self.root, text="Show Images Table", command=self.create_images_table_screen, style='Custom.TButton')
        button_show_images_table.pack(pady=10)
        self.root.mainloop()  # Start the main event loop
