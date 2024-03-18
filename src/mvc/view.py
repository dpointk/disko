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
            self.display_image_data(selected_cluster)  # Display image data for the selected cluster
            self.create_images_table_screen(selected_cluster)  # Create images table for the selected cluster
        else:
            messagebox.showerror("Error", "Please select a cluster.")  # Show error message if no cluster selected

    def create_images_table_screen(self, selected_cluster):
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
        image_data = self.db.select_all(selected_cluster)

        # Populate the treeview with image data
        for image in image_data:
            self.treeview.insert('', 'end', values=(image[0], image[1]))  # Insert image data into the treeview

    def update_columns(self):
        # Update column display based on checkbox selection
        selected_columns = [column.get() for column in self.checkboxes.values()]
        for col in self.columns:
            if col in selected_columns:
                self.treeview.column(col, display=True)
            else:
                self.treeview.column(col, display=False)

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

        self.root.mainloop()  # Start the main event loop
