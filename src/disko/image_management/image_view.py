import tkinter as tk
from tkinter import ttk, messagebox
from src.disko.sqlite import SQLiteCRUD

class ImageRegistryManager:
    def __init__(self):
        self.treeview = None  # Initialize treeview widget
        self.db = SQLiteCRUD('image_data.db')  # Initialize SQLiteCRUD instance

    def display_image_data(self, selected_cluster, registry_amount, treeview):
        # Clear existing data in the treeview
        for row in treeview.get_children():
            treeview.delete(row)

        # Populate the treeview with the data
        for registry, num_images in registry_amount.items():
            # Insert the data into the treeview
            treeview.insert('', 'end', values=(selected_cluster, registry, num_images))


    def create_images_table_screen(self, root, selected_cluster):
        # Create a new window for displaying images table
        images_table_window = tk.Toplevel(root)
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
        if selected_cluster:
            image_data = self.db.select_all('images')
            # Populate the treeview with image data
            for image in image_data:
                self.treeview.insert('', 'end', values=(image[1], image[2]))  # Insert image data into the treeview
        else:
            messagebox.showerror("Error", "No cluster selected.")  # Show error message if no cluster is selected

    def update_columns(self, checkboxes, columns):
        # Update column display based on checkbox selection
        selected_columns = [column.get() for column in checkboxes.values()]
        for col in columns:
            if col in selected_columns:
                self.treeview.column(col, display=True)
            else:
                self.treeview.column(col, display=False)
    
