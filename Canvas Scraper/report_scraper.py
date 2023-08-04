# report_scraper.py

# import necessary libraries 
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from canvas_scraper import CanvasScraper
from event_handler import MyHandler

# This class extends the existing Scraper class
class ReportScraper(CanvasScraper):
    def __init__(self, download_path, links_path):
        # Initialize variables
        options = ChromeOptions()
        options.use_chromium = True
        options.add_experimental_option("prefs", {
        "download.default_directory": download_path

        })

        # provide the path to the installed webdriver here:
        self.driver = webdriver.Chrome(options=options)

        self.download_path = download_path
        self.assignment_df = pd.read_csv(links_path)
        self.instructors = self.assignment_df["College Course"].str[13:]
        self.urls = self.assignment_df["Canvas Link"]
        # Hashset filled with unique urls that have been looped through
        self.url_set = set()

    # This function will rename the latest file added to a specified directory    
    def rename_latest_file(self, directory, course_name):
        """
        Rename the most recent file in the specified directory to the specified filename.
        
        Args:
            directory (str): The directory containing the files to rename.
            course_name (str): The string to prepend to the filename.
        """
        # Get list of files in directory
        files = [os.path.join(directory, filename) for filename in os.listdir(directory)]
        
        # Sort files by modification time (most recent first)
        files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        # Rename most recent file to new filename
        most_recent_file = files[0]
        old_filename = os.path.basename(most_recent_file)  # Extract the filename from the path
        new_filename = course_name + " " + old_filename  # Prepend the course_name to the filename
        os.rename(most_recent_file, os.path.join(directory, new_filename))

    def wait_for_file(self, initial_files, directory, timeout=300):
        # Get the current time
        start_time = time.time()

        # Start a loop that will run until timout has passed
        while True:
            # Get a set of all files currently in the directory
            current_files = set(os.listdir(directory))
            # Subtract the initial set of files from the current set to find any new files
            new_files = current_files - initial_files

            # Print the current files and the new files
            print(f"Current files: {current_files}")
            print(f"New files: {new_files}")

            # If there are any new files, return True
            if new_files:
                return True

            # If the timeout has been exceeded, return False
            if time.time() - start_time > timeout:
                return False

            # Sleep for 1 second before repeating the loop
            time.sleep(1)

    def generate_report(self, i):
        # try finding summary statistics if report already generated
        try:
            # Get initial set of files in the directory
            initial_files = set(os.listdir(self.download_path))

            # Initiate the file download
            student_analysis = self.driver.find_element("xpath", '//*[@id="summary-statistics"]/header/div/div[2]/div/a/span[2]').click()
            
            time.sleep(3)

            # Wait for the file to be downloaded
            if self.wait_for_file(initial_files, directory=self.download_path):
                course_name = self.instructors[i]
                self.rename_latest_file(self.download_path, course_name)

        # if report hasn't been generated yet, click button and wait for report to generate
        except:
            student_analysis = self.driver.find_element("xpath", '//*[@id="summary-statistics"]/header/div/div[2]/div/button').click()
            # check if file has been downloaded then rename
            if self.wait_for_file(self.download_path):
                course_name = self.instructors[i] 
                self.rename_latest_file(directory=self.download_path, course_name=course_name)
            else:
                print(self.instructors[i] + " timed out. Did not download report")
            
    # Use hashset to store unique urls. If the url has been added, 
    def check_duplicate_urls(self, url):
        if url in self.url_set:
            print(f"Duplicate URL found: {url}")
            return True
        else:
            self.url_set.add(url)
            return False
    
    # This is the main function that will execute the webscraper
    def scrape_reports(self):
        # this list will keep track of which instructors don't have quiz statistics
        no_stats = []

        # do log in process
        self.login(self.urls[0])

        for i in range(len(self.urls)):
            # Check if link has already been iterated through
            if self.check_duplicate_urls(url=self.urls[i]):
                continue

            # Go to target page
            self.driver.get(self.urls[i])

            # Wait for 3 seconds to fully load
            time.sleep(3)
            
            # Locate the quiz statistics button and click
            stats_xpath = "/html/body/div[3]/div[2]/div[2]/div[3]/div[2]/aside/div/ul/li[1]/a"
            quiz_statistics = self.driver.find_element("xpath", stats_xpath).click()
            time.sleep(3)

            # try to see if the instructor has a quiz statistics report
            try:
                # call generate_report to find summary statistics if report already generated
                self.generate_report(i)
            except:
                no_stats.append(i)
            
            time.sleep(5)

        print("\n\n")
        print("Instructor indices with no statistics:")
        for n in no_stats:
            print(self.instructors[n])
        print("\nScript Complete!")

        # Close the driver
        self.driver.close()