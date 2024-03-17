import tkinter as tk
from tkinter import ttk
from src.disko.sqlite import SQLiteCRUD

db = SQLiteCRUD('image_data.db')

def display_image_data():
    # Clear previous data in the table
    for row in treeview.get_children():
        treeview.delete(row)
    # Retrieve image data from the database
    image_data = db.select_all("registries")
    # Populate the table with image data
    for image in image_data:
        treeview.insert('', 'end', values=image)

def create_images_table_screen():
    # Create a new window for displaying the images table
    images_table_window = tk.Toplevel(root)
    images_table_window.title("Images Table")

    # Create a frame for the table
    frame = ttk.Frame(images_table_window, style='DarkFrame.TFrame')
    frame.pack(padx=20, pady=20)

    # Define column names
    columns = ['Registry Name', 'Number of images', 'Percentage']

    # Create a Treeview widget to display the table
    treeview = ttk.Treeview(frame, columns=columns, show='headings', style='Custom.Treeview')
    for col in columns:
        treeview.heading(col, text=col)

    treeview.pack(side='left', fill='both', expand=True)

    # Add scrollbar to the table
    scrollbar = ttk.Scrollbar(frame, orient='vertical', command=treeview.yview)
    scrollbar.pack(side='right', fill='y')
    treeview.configure(yscrollcommand=scrollbar.set)

    # Display image data in the table
    display_image_data()

def update_columns():
    selected_columns = [column.get() for column in checkboxes.values()]
    for col in columns:
        if col in selected_columns:
            treeview.column(col, display=True)
        else:
            treeview.column(col, display=False)

# Create the main window
root = tk.Tk()
root.title("Image Registry Manager")

# Define custom styles
root.style = ttk.Style()
root.style.theme_use('clam')  # Change the theme

root.style.configure('DarkFrame.TFrame', background='#363636')  # Dark grey background
root.style.configure('Custom.Treeview', background='#363636', foreground='white', fieldbackground='#363636', font=('Arial', 10))  # Customizing Treeview colors

# Create a frame for the table
frame = ttk.Frame(root, style='DarkFrame.TFrame')
frame.pack(padx=100, pady=100)

# Define column names
columns = ['Registry Name', 'Number of images', 'Percentage']

# Create a Treeview widget to display the table
treeview = ttk.Treeview(frame, columns=columns, show='headings', style='Custom.Treeview')
for col in columns:
    treeview.heading(col, text=col)

treeview.pack(side='left', fill='both', expand=True)

# Add scrollbar to the table
scrollbar = ttk.Scrollbar(frame, orient='vertical', command=treeview.yview)
scrollbar.pack(side='right', fill='y')
treeview.configure(yscrollcommand=scrollbar.set)

# Create checkboxes to select columns
checkbox_frame = ttk.Frame(root, style='DarkFrame.TFrame')
checkbox_frame.pack(pady=10)

checkboxes = {}
for col in columns:
    var = tk.BooleanVar()
    var.set(True)  # Default: all columns visible
    checkboxes[col] = var
    checkbox = ttk.Checkbutton(checkbox_frame, text=col, variable=var, command=update_columns, style='Custom.TCheckbutton')
    checkbox.pack(side='left')

# Create a button to display data
button_display_data = ttk.Button(root, text="Display Data", command=display_image_data, style='Custom.TButton')
button_display_data.pack(pady=10)

# Create a button to open another screen and display images table
button_show_images_table = ttk.Button(root, text="Show Images Table", command=create_images_table_screen, style='Custom.TButton')
button_show_images_table.pack(pady=10)

# Run the GUI application
root.mainloop()
