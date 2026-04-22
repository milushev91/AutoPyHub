import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import os
import shutil

# -------------------------
# Functions (top of file)
# -------------------------

# Function to center the window on the screen
def center_window(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

# Function to browse for folder
def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder_selected)

# Function to organize files
def organize_files():
    folder = path_entry.get()

    # Validate folder BEFORE showing "Organizing..."
    if not folder or not os.path.isdir(folder):
        messagebox.showerror("Error", "Please select a valid folder.")
        status_label.config(text="Invalid folder", fg="red")
        return

    # Now it's safe to show "Organizing..."
    status_label.config(text="Organizing...", fg="blue")
    root.update_idletasks()

    try:
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        total_files = len(files)

        progress["value"] = 0
        progress["maximum"] = total_files
        root.update_idletasks()

        for index, filename in enumerate(files, start=1):
            file_path = os.path.join(folder, filename)

            # Get file extension
            file_ext = filename.split('.')[-1].lower()
            target_folder = os.path.join(folder, file_ext.upper())

            # Create folder if it doesn't exist
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            # Move file
            shutil.move(file_path, os.path.join(target_folder, filename))

            # Update progress bar
            progress["value"] = index
            root.update_idletasks()

        progress["value"] = total_files
        messagebox.showinfo("Success", "Files organized successfully!")
        status_label.config(text="Done!", fg="green")
        
    except Exception as e:
        progress["value"] = 0
        messagebox.showerror("Error", f"An error occurred:\n{e}")
        status_label.config(text="Error occurred", fg="red")

def open_folder():
    folder = path_entry.get()

    if not folder or not os.path.isdir(folder):
        messagebox.showerror("Error", "Please select a valid folder.")
        status_label.config(text="Invalid folder", fg="red")
        return

    try:
        os.startfile(folder)  # Windows only
        status_label.config(text="Folder opened", fg="green")

    except Exception as e:
        messagebox.showerror("Error", f"Cannot open folder:\n{e}")
        

# -------------------------
# GUI Setup
# -------------------------

# Create main window
root = tk.Tk()
root.iconbitmap("app-icon.ico")  # Set your icon file here

#Create window title and set window size
root.title("File Organizer")
root.geometry("500x300")
root.resizable(False, False)
center_window(root)

# Set background color for the whole window
root.configure(bg="#f2f2f2")

main_frame = tk.Frame(root, bg="#f2f2f2")
main_frame.pack(pady=10)

# Label for folder path
path_label = tk.Label(main_frame, text="Folder Path:", bg="#f2f2f2", font=("Arial", 12))
path_label.pack(pady=5)

# Label for folder path
path_entry = tk.Entry(main_frame, width=50, font=("Arial", 12))
path_entry.pack(pady=5)

# Browse Button
browse_button = tk.Button(main_frame, text="Browse", command=browse_folder, font=("Arial", 11))
browse_button.pack(pady=8)

# Start Button
start_button = tk.Button(main_frame, text="Start Organizing", command=organize_files, font=("Arial", 11))
start_button.pack(pady=8)

# Open Folder Button
open_button = tk.Button(main_frame, text="Open Folder", command=open_folder, font=("Arial", 11))
open_button.pack(pady=8)

# Status Label
status_label = tk.Label(main_frame, text="Ready", font=("Arial", 11), fg="green")
status_label.pack(pady=4)

# Progress Bar
progress = ttk.Progressbar(main_frame, orient="horizontal", length=450, mode="determinate")
progress.pack(pady=4)

# -------------------------
# Main Loop
# -------------------------
# Start the GUI event loop
root.mainloop()

