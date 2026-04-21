import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import shutil

# -------------------------
# Functions (top of file)
# -------------------------

# Function to browse for folder
def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder_selected)

def organize_files():
    folder = path_entry.get()

    if not folder or not os.path.isdir(folder):
        messagebox.showerror("Error", "Please select a valid folder.")
        return

    try:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)

            # Skip folders
            if os.path.isdir(file_path):
                continue

            # Get file extension
            file_ext = filename.split('.')[-1].lower()
            target_folder = os.path.join(folder, file_ext.upper())

            # Create folder if it doesn't exist
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            # Move file
            shutil.move(file_path, os.path.join(target_folder, filename))

        messagebox.showinfo("Success", "Files organized successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

# -------------------------
# GUI Setup
# -------------------------

# Create main window
root = tk.Tk()

#Create window title and set window size
root.title("File Organizer")
root.geometry("500x200")

# Label for folder path
path_label = tk.Label(root, text="Folder Path:", font=("Arial", 12))
path_label.pack(pady=5)

# Label for folder path
path_entry = tk.Entry(root, width=50, font=("Arial", 12))
path_entry.pack(pady=5)

# Browse Button
browse_button = tk.Button(root, text="Browse", command=browse_folder, font=("Arial", 11))
browse_button.pack(pady=5)

# Start Button
start_button = tk.Button(root, text="Start Organizing", command=organize_files, font=("Arial", 11))
start_button.pack(pady=10)

# -------------------------
# Main Loop
# -------------------------
# Start the GUI event loop
root.mainloop()

