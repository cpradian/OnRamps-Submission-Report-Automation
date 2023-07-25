import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from report_scraper import ReportScraper

class WebScraperGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Web Scraper")
        self.window.geometry("525x200")

        # set the background color of the window
        self.window.configure(bg="black")

        # center the window
        self.window.eval('tk::PlaceWindow %s center' % self.window.winfo_toplevel())

        # style the widgets to look more modern
        
        style = ttk.Style()
        style.configure('TLabel', font=('Helvetica Neue', 10), background="black", foreground="white")
        style.configure('TButton', font=('Helvetica Neue', 10), padding=1, background="black")
        style.configure('TEntry', font=('Helvetica Neue', 10), background="gray", foreground="black")
        style.configure('TCombobox', font=('Helvetica Neue', 10), padding=4, background="white", foreground="black")

        # webdriver path
        webdriver_label = ttk.Label(self.window, text="Webdriver Path:")
        webdriver_label.grid(column=0, row=0, padx=5, pady=5)

        self.webdriver_path = tk.StringVar()
        webdriver_entry = ttk.Entry(self.window, width=40, textvariable=self.webdriver_path)
        webdriver_entry.grid(column=1, row=0, padx=5, pady=5)

        webdriver_browse_button = ttk.Button(self.window, text="Browse", command=self.browse_webdriver)
        webdriver_browse_button.grid(column=2, row=0, padx=5, pady=5)

        # csv file path
        csv_label = ttk.Label(self.window, text="CSV File Path:")
        csv_label.grid(column=0, row=1, padx=5, pady=5)

        self.csv_path = tk.StringVar()
        csv_entry = ttk.Entry(self.window, width=40, textvariable=self.csv_path)
        csv_entry.grid(column=1, row=1, padx=5, pady=5)

        csv_browse_button = ttk.Button(self.window, text="Browse", command=self.browse_csv)
        csv_browse_button.grid(column=2, row=1, padx=5, pady=5)

        # download file path
        download_label = ttk.Label(self.window, text="Download Directory:")
        download_label.grid(column=0, row=2, padx=5, pady=5)

        self.download_path = tk.StringVar()
        download_entry = ttk.Entry(self.window, width=40, textvariable=self.download_path)
        download_entry.grid(column=1, row=2, padx=5, pady=5)

        download_browse_button = ttk.Button(self.window, text="Browse", command=self.browse_download)
        download_browse_button.grid(column=2, row=2, padx=5, pady=5)

        # lab selection
        lab_label = ttk.Label(self.window, text="Select Lab:")
        lab_label.grid(column=0, row=3, padx=5, pady=5)

        self.lab_options = ["Post-Lab 1", "Post-Lab 2", "Post-Lab 3", "Post-Lab 4", "Post-Lab 5", "Post-Lab 6", "Post-Lab 7", "Post-Lab 8"]
        self.selected_lab = tk.StringVar()
        self.selected_lab.set(self.lab_options[0])
        lab_dropdown = ttk.Combobox(self.window, textvariable=self.selected_lab, values=self.lab_options, width=10)
        lab_dropdown.grid(column=1, row=3, padx=5, pady=5)

        # start button
        start_button = ttk.Button(self.window, text="Start", command=self.start_scraper)
        start_button.grid(column=1, row=4, padx=5, pady=5)

        # center the widgets in the window
        for child in self.window.winfo_children():
            child.grid_configure(padx=10, pady=5)

        self.window.mainloop()

    def browse_webdriver(self):
        filepath = filedialog.askopenfilename()
        self.webdriver_path.set(filepath)

    def browse_csv(self):
        filepath = filedialog.askopenfilename()
        self.csv_path.set(filepath)

    def browse_download(self):
        filepath = filedialog.askdirectory()
        self.download_path.set(filepath)

    def start_scraper(self):
        # Get information from text fields
        driver_path = self.webdriver_path.get()
        download_path = self.download_path.get()
        postlab_links_dir = self.csv_path.get()
        
        lab_num = self.selected_lab.get()
        scraper = ReportScraper(driver_path, download_path, postlab_links_dir, lab_num)
        scraper.scrape_reports()
        # canvas_scraper(driver_path, download_path, postlab_links_dir, lab_num)

WebScraperGUI()