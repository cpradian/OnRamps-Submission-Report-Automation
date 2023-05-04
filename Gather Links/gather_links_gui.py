import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import gather_links
from gather_links import run_gather_links

def browse_file_path():
    file_path = filedialog.askopenfilename()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, file_path)

def browse_webdriver_path():
    file_path = filedialog.askopenfilename()
    webdriver_path_entry.delete(0, tk.END)
    webdriver_path_entry.insert(0, file_path)

def run_script():
    file_path = path_entry.get()
    webdriver_path = webdriver_path_entry.get()
    if os.path.isfile(file_path) and os.path.isfile(webdriver_path):
        # Replace this with your script's logic
        print(f"Running Gather Links Script")
        run_gather_links(webdriver_path, file_path)
    else:
        print("Invalid file path(s)")

# Define GUI and its items

root = tk.Tk()
root.geometry("600x200")
root.configure(bg="#212121")
root.title("Gather Post-Lab Links")
root.resizable(False, False)


webdriver_path_frame = tk.Frame(root, bg="#212121")
webdriver_path_frame.pack(fill=tk.X, padx=20, pady=20)

webdriver_path_label = tk.Label(webdriver_path_frame, text="Path to WebDriver:     ", fg="white", bg="#212121")
webdriver_path_label.pack(side=tk.LEFT)

webdriver_path_entry = tk.Entry(webdriver_path_frame, width=50, bg="white", fg="black")
webdriver_path_entry.pack(side=tk.LEFT, padx=10, expand=True)

webdriver_browse_button = tk.Button(webdriver_path_frame, text="Browse", bg="#757575", fg="white", command=browse_webdriver_path)
webdriver_browse_button.pack(side=tk.LEFT, padx=10)

path_frame = tk.Frame(root, bg="#212121")
path_frame.pack(fill=tk.X, padx=20, pady=20)

path_label = tk.Label(path_frame, text="Path to General Links:", fg="white", bg="#212121")
path_label.pack(side=tk.LEFT)

path_entry = tk.Entry(path_frame, width=50, bg="white", fg="black")
path_entry.pack(side=tk.LEFT, padx=10, expand=True)

browse_button = tk.Button(path_frame, text="Browse", bg="#757575", fg="white", command=browse_file_path)
browse_button.pack(side=tk.LEFT, padx=10)


run_button = tk.Button(root, text="Run Script", bg="#757575", fg="white", command=run_script)
run_button.pack(pady=10)

root.mainloop()
