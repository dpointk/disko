import tkinter as tk
from tkinter import ttk
from src.disko.sqlite import SQLiteCRUD
from src.mvc.controller import ImageController

# Class for GUI
class ImageRegistryManager:
    def __init__(self, db_file):
        self.db = SQLiteCRUD(db_file)
        self.root = tk.Tk()
        self.root.title("Image Registry Manager")
        self.root.style = ttk.Style()
        self.root.style.theme_use('clam')
        self.columns = ['Registry Name', 'Number of images', 'Percentage']
        self.treeview = None
        self.checkboxes = {col: tk.BooleanVar(value=True) for col in self.columns}
        self.controller = ImageController(db_file)

    # display the image data
    def display_image_data(self):
        for row in self.treeview.get_children():
            self.treeview.delete(row)
        percentages = self.controller.calculate_percentages(self.db)
        for data in percentages:
            self.treeview.insert('', 'end', values=(data[0], data[1], f"{data[2]:.0f}%"))

    # create the images table screen
    def create_images_table_screen(self):
        images_table_window = tk.Toplevel(self.root)
        images_table_window.title("Images Table")
        frame = ttk.Frame(images_table_window, style='DarkFrame.TFrame')
        frame.pack(padx=20, pady=20)
        self.treeview = ttk.Treeview(frame, columns=self.columns, show='headings', style='Custom.Treeview')
        for col in self.columns:
            self.treeview.heading(col, text=col)
        self.treeview.pack(side='left', fill='both', expand=True)
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.treeview.yview)
        scrollbar.pack(side='right', fill='y')
        self.treeview.configure(yscrollcommand=scrollbar.set)
        for row in self.treeview.get_children():
            self.treeview.delete(row)
        image_data = self.db.select_all("images")
        for image in image_data:
            self.treeview.insert('', 'end', values=image)

    # update the columns
    def update_columns(self):
        selected_columns = [column.get() for column in self.checkboxes.values()]
        for col in self.columns:
            if col in selected_columns:
                self.treeview.column(col, display=True)
            else:
                self.treeview.column(col, display=False)

    # run the GUI
    def run(self):
        frame = ttk.Frame(self.root, style='DarkFrame.TFrame')
        frame.pack(padx=100, pady=100)
        self.treeview = ttk.Treeview(frame, columns=self.columns, show='headings', style='Custom.Treeview')
        for col in self.columns:
            self.treeview.heading(col, text=col)
        self.treeview.pack(side='left', fill='both', expand=True)
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.treeview.yview)
        scrollbar.pack(side='right', fill='y')
        self.treeview.configure(yscrollcommand=scrollbar.set)
        checkbox_frame = ttk.Frame(self.root, style='DarkFrame.TFrame')
        checkbox_frame.pack(pady=10)
        for col in self.columns:
            checkbox = ttk.Checkbutton(checkbox_frame, text=col, variable=self.checkboxes[col], command=self.update_columns, style='Custom.TCheckbutton')
            checkbox.pack(side='left')
        button_display_data = ttk.Button(self.root, text="Display Data", command=self.display_image_data, style='Custom.TButton')
        button_display_data.pack(pady=10)
        button_show_images_table = ttk.Button(self.root, text="Show Images Table", command=self.create_images_table_screen, style='Custom.TButton')
        button_show_images_table.pack(pady=10)
        self.root.mainloop()