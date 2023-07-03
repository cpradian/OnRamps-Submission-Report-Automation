# report_scraper.py

# import necessary libraries 
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import pandas as pd

from canvas_scraper import CanvasScraper

# This class extends the existing Scraper class
class ReportScraper(CanvasScraper):

    def __init__(self, driver_path, download_path, postlab_links_dir, lab_num):
        # Initialize variables
        self.download_path = download_path
        self.postlab_links_dir = postlab_links_dir
        self.lab_num = lab_num

        # specify the download directory
        options = EdgeOptions()
        options.use_chromium = True
        options.add_experimental_option("prefs", {
        # change download directory here:
        "download.default_directory": self.download_path
        })

        # provide the path to the installed webdriver here:
        self.driver = webdriver.Edge(executable_path=driver_path, options=options)

        # read csv file to get list of links
        # provide path to csv file w/ links here:
        self.dataset = pd.read_csv(self.postlab_links_dir)

        # Grab only the column with the links and make an array
        lab = self.lab_num + " Link"
        self.urls = self.dataset[lab]

        self.instructors = self.dataset['Instructor']

    # This function will rename the latest file added to a specified directory    
    def rename_latest_file(self, directory, new_filename):
        """
        Rename the most recent file in the specified directory to the specified filename.
        
        Args:
            directory (str): The directory containing the files to rename.
            new_filename (str): The new filename to give to the most recent file.
        """
        # Get list of files in directory
        files = [os.path.join(directory, filename) for filename in os.listdir(directory)]
        
        # Sort files by modification time (most recent first)
        files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        # Rename most recent file to new filename
        most_recent_file = files[0]
        os.rename(most_recent_file, os.path.join(directory, new_filename))

    # This function will wait a maximum of 300 seconds for the report to generate and download
    def wait_for_file(self, directory, filename, timeout=300):
        """
        Wait for the specified file to appear in the specified directory.
        
        Args:
            directory (str): The directory to check for the file.
            filename (str): The name of the file to check for.
            timeout (int): The maximum amount of time to wait for the file to appear, in seconds.
            
        Returns:
            bool: True if the file was found before the timeout, False otherwise.
        """
        start_time = time.time()
        while True:
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                return True
            if time.time() - start_time > timeout:
                return False
            time.sleep(1)
    
    # This function will check if a report is already generated
    # If it is already generated, it will download. If not, it will call the wait_for_file function
    def generate_report(self, i):
        # try finding summary statistics if report already generated
        try:
            student_analysis = self.driver.find_element("xpath", '//*[@id="summary-statistics"]/header/div/div[2]/div/a/span[2]').click()
            time.sleep(1)
            # check if file has been downloaded and rename
            old_name = self.lab_num + r" Quiz Student Analysis Report.csv"
            if self.wait_for_file(self.download_path, old_name):
                new_name = self.instructors[i] + " " + self.lab_num + r" Quiz Student Analysis Report.csv"
                self.rename_latest_file(self.download_path, new_name)
            else:
                print(self.instructors[i] + " timed out. Did not download report")
        # if report hasn't been generated yet, click button and wait for report to generate
        except:
            student_analysis = self.driver.find_element("xpath", '//*[@id="summary-statistics"]/header/div/div[2]/div/button').click()
            # check if file has been downloaded then rename
            old_name = self.lab_num + r" Quiz Student Analysis Report.csv"
            if self.wait_for_file(self.download_path, old_name):
                new_name = self.instructors[i] + " " + self.lab_num + r" Quiz Student Analysis Report.csv"
                self.rename_latest_file(self.download_path, new_name)
            else:
                print(self.instructors[i] + " timed out. Did not download report")

    # This is the main function that will execute the webscraper
    def scrape_reports(self):
        # this list will keep track of which instructors don't have quiz statistics
        no_stats = []

        # do log in process
        self.login(self.urls[0])

        for i in range(len(self.urls)):
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

            

