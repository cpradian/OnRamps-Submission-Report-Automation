from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt
from report_scraper import ReportScraper

class WebScraperGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("Web Scraper")
        self.setGeometry(100, 100, 600, 200)  # adjust the width and height as per your needs

        # main widget and layout
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # webdriver path
        webdriver_layout = QHBoxLayout()
        self.webdriver_label = QLabel("Webdriver Path:", self)
        self.webdriver_label.setFixedWidth(135)
        webdriver_layout.addWidget(self.webdriver_label)

        self.webdriver_entry = QLineEdit(self)
        webdriver_layout.addWidget(self.webdriver_entry)

        self.webdriver_browse_button = QPushButton("Browse", self)
        self.webdriver_browse_button.setFixedWidth(75)
        self.webdriver_browse_button.clicked.connect(self.browse_webdriver)
        webdriver_layout.addWidget(self.webdriver_browse_button)
        
        layout.addLayout(webdriver_layout)

        # csv file path
        csv_layout = QHBoxLayout()
        self.csv_label = QLabel("CSV File Path:", self)
        self.csv_label.setFixedWidth(135)
        csv_layout.addWidget(self.csv_label)

        self.csv_entry = QLineEdit(self)
        csv_layout.addWidget(self.csv_entry)

        self.csv_browse_button = QPushButton("Browse", self)
        self.csv_browse_button.setFixedWidth(75)
        self.csv_browse_button.clicked.connect(self.browse_csv)
        csv_layout.addWidget(self.csv_browse_button)

        layout.addLayout(csv_layout)

        # download file path
        download_layout = QHBoxLayout()
        self.download_label = QLabel("Download Directory:", self)
        self.download_label.setFixedWidth(135)
        download_layout.addWidget(self.download_label)

        self.download_entry = QLineEdit(self)
        download_layout.addWidget(self.download_entry)

        self.download_browse_button = QPushButton("Browse", self)
        self.download_browse_button.setFixedWidth(75)
        self.download_browse_button.clicked.connect(self.browse_download)
        download_layout.addWidget(self.download_browse_button)

        layout.addLayout(download_layout)

        # start button
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_scraper)
        layout.addWidget(self.start_button)

    def browse_webdriver(self):
        filepath, _ = QFileDialog.getOpenFileName()
        if filepath:
            self.webdriver_entry.setText(filepath)

    def browse_csv(self):
        filepath, _ = QFileDialog.getOpenFileName()
        if filepath:
            self.csv_entry.setText(filepath)

    def browse_download(self):
        filepath = QFileDialog.getExistingDirectory()
        if filepath:
            self.download_entry.setText(filepath)

    def start_scraper(self):
        # Get information from text fields
        driver_path = self.webdriver_entry.text()
        download_path = self.download_entry.text()
        postlab_links_dir = self.csv_entry.text()
        
        scraper = ReportScraper(driver_path, download_path, postlab_links_dir)
        scraper.scrape_reports()

if __name__ == "__main__":
    app = QApplication([])
    window = WebScraperGUI()
    window.show()
    app.exec_()
