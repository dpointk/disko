import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # Importing messagebox for error handling
from src.disko.sqlite import SQLiteCRUD
from src.mvc.controller import ImageController

# Class for GUI
class ImageRegistryManager:
    def __init__(self, db_file):
        # Initialize the SQLiteCRUD instance for database operations
        self.db = SQLiteCRUD(db_file)
        
        # Create the main Tkinter window
        self.root = tk.Tk()
        self.root.title("Image Registry Manager")
        
        # Apply the 'clam' theme to the GUI
        self.root.style = ttk.Style()
        self.root.style.theme_use('clam')
        
        # Define columns for the images table
        self.columns = ['Registry Name', 'Number of images', 'Percentage']
        
        # Initialize treeview, checkboxes, and ImageController
        self.treeview = None
        self.checkboxes = {col: tk.BooleanVar(value=True) for col in self.columns}
        self.controller = ImageController(db_file)

    # Method to display the image data in the treeview
    def display_image_data(self):
        for row in self.treeview.get_children():
            self.treeview.delete(row)
        percentages = self.controller.calculate_percentages()
        for data in percentages:
            self.treeview.insert('', 'end', values=(data[0], data[1], f"{data[2]:.0f}%"))

    # Method to create the cluster selection screen
    def cluster_selection(self, clusters):
        # Open a new window for cluster selection
        cluster_selection_window = tk.Toplevel(self.root)
        cluster_selection_window.title("Cluster Selection")

        # Add widgets for cluster selection
        label = ttk.Label(cluster_selection_window, text="Please select a cluster:")
        label.pack()

        # Create a Combobox for cluster selection
        cluster_var = tk.StringVar()
        cluster_combobox = ttk.Combobox(cluster_selection_window, textvariable=cluster_var, values=clusters)
        cluster_combobox.pack()

        # Create a button to confirm cluster selection
        confirm_button = ttk.Button(cluster_selection_window, text="Confirm", command=lambda: self.confirm_cluster_selection(cluster_var.get(), cluster_selection_window))
        confirm_button.pack()

    # Method to confirm cluster selection and open the images table screen
    def confirm_cluster_selection(self, selected_cluster, cluster_selection_window):
        if selected_cluster:
            cluster_selection_window.destroy()  # Close the cluster selection window
            #self.create_images_table_screen()    # Open the images table screen with the selected cluster
            self.display_image_data()            # Automatically display image data
        else:
            messagebox.showerror("Error", "Please select a cluster.")

    # Method to create the images table screen
    def create_images_table_screen(self):
        images_table_window = tk.Toplevel(self.root)
        images_table_window.title("Images Table")
        frame = ttk.Frame(images_table_window, style='DarkFrame.TFrame')
        frame.pack(padx=20, pady=20)
        
        # Create a Treeview widget for displaying images table
        self.treeview = ttk.Treeview(frame, columns=self.columns, show='headings', style='Custom.Treeview')
        for col in self.columns:
            self.treeview.heading(col, text=col)
        self.treeview.pack(side='left', fill='both', expand=True)
        
        # Add scrollbar to the treeview
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.treeview.yview)
        scrollbar.pack(side='right', fill='y')
        self.treeview.configure(yscrollcommand=scrollbar.set)
        
        # Fetch image data from the database and populate the treeview
        for row in self.treeview.get_children():
            self.treeview.delete(row)
        image_data = self.db.select_all("images")
        for image in image_data:
            self.treeview.insert('', 'end', values=image)

    # Method to update the columns based on checkbox selection
    def update_columns(self):
        selected_columns = [column.get() for column in self.checkboxes.values()]
        for col in self.columns:
            if col in selected_columns:
                self.treeview.column(col, display=True)
            else:
                self.treeview.column(col, display=False)

    # Method to run the GUI
    def run(self):
        # Create the main frame
        frame = ttk.Frame(self.root, style='DarkFrame.TFrame')
        frame.pack(padx=100, pady=100)
        
        # Create a Treeview widget for the main frame
        self.treeview = ttk.Treeview(frame, columns=self.columns, show='headings', style='Custom.Treeview')
        for col in self.columns:
            self.treeview.heading(col, text=col)
        self.treeview.pack(side='left', fill='both', expand=True)
        
        # Add scrollbar to the treeview
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.treeview.yview)
        scrollbar.pack(side='right', fill='y')
        self.treeview.configure(yscrollcommand=scrollbar.set)
        
        # Create checkboxes for column selection
        checkbox_frame = ttk.Frame(self.root, style='DarkFrame.TFrame')
        checkbox_frame.pack(pady=10)
        for col in self.columns:
            checkbox = ttk.Checkbutton(checkbox_frame, text=col, variable=self.checkboxes[col], command=self.update_columns, style='Custom.TCheckbutton')
            checkbox.pack(side='left')
        
        # Add buttons for cluster selection, displaying data, and showing images table
        button_show_images_table = ttk.Button(self.root, text="Select Cluster", command=self.cluster_selection, style='Custom.TButton')
        button_show_images_table.pack(pady=10)
        
        button_display_data = ttk.Button(self.root, text="Display Data", command=self.display_image_data, style='Custom.TButton')
        button_display_data.pack(pady=10)

        button_show_images_table = ttk.Button(self.root, text="Show Images Table", command=self.create_images_table_screen, style='Custom.TButton')
        button_show_images_table.pack(pady=10)
        
        # Run the main event lo
        self.root.mainloop()
