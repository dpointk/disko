import tkinter as tk
from tkinter import ttk

class ImageRegistryManager:
    def __init__(self):
        self.root = tk.Tk()  # Tkinter root window
        self.root.title("Image Registry Manager")  # Window title
        self.root.style = ttk.Style()  # Tkinter style
        self.root.style.theme_use('clam')  # Use 'clam' theme
        self.columns = ['Registry Name', 'Number of Images']  # Table columns
        self.treeview = None  # Treeview widget
        # Checkbox variables for each column
        self.checkboxes = {col: tk.BooleanVar(value=True) for col in self.columns}


    def display_image_data(self, registry_amount):
        # Clear existing data in the treeview
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        # Populate the treeview with the data
        for registry, num_images in registry_amount.items():
            # Insert the data into the treeview
            self.treeview.insert('', 'end', values=(registry, num_images))


    def create_images_table_screen(self, image_data):
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

        # Populate the treeview with image data
        for image in image_data:
            self.treeview.insert('', 'end', values=(image[0], image[1]))  # Insert image data into the treeviewd

    def update_columns(self):
        # Update column display based on checkbox selection
        selected_columns = [column.get() for column in self.checkboxes.values()]
        for col in self.columns:
            if col in selected_columns:
                self.treeview.column(col, display=True)
            else:
                self.treeview.column(col, display=False)
    

    def run_gui(self, registry_amount, image_data):
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

        # Display image data
        self.display_image_data(registry_amount)

        # Add buttons for displaying data, and showing images table
        button_show_images_table = ttk.Button(self.root, text="Show Images Table", command=lambda: self.create_images_table_screen(image_data), style='Custom.TButton')
        button_show_images_table.pack(pady=10)
        self.root.mainloop()  # Start the main event loop
