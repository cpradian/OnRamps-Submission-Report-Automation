# import necessary libraries 
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


# specify the download directory
options = ChromeOptions()

options = ChromeOptions()
options.use_chromium = True
options.add_experimental_option("prefs", {
  # change download directory here:
  "download.default_directory": r"C:\Users\Calvin Pradian\Box\22-23 PHY Student Graders\PHY 22-23 Lab Submission Reports\Lab 3 Test"
  
})

# provide the path to the installed webdriver here:
driver = webdriver.Chrome(executable_path=r"C:\Users\Calvin Pradian\Documents\OnRamps\Web Scraper\msedgedriver.exe", options=options)


# read csv file to get list of links
# provide path to csv file w/ links here:
dataset = pd.read_csv(r"C:\Users\Calvin Pradian\Documents\OnRamps\Gather Links Instructions\Post-Lab Links.csv")

# Grab only the column with the links and make an array
# Specify which Post Lab # here:
urls = dataset["Post Lab 3 Link"]

# this list will keep track of which instructors don't have quiz statistics
no_stats = []

# do log in process
driver.get(urls[0])
# allow 30 seconds to complete login process
time.sleep(30) 

for i in range(len(urls)):
    # Go to target page
    driver.get(urls[i])
    # Wait for 5 seconds to fully load
    time.sleep(3)
    # Locate the quiz statistics button and click
    quiz_statistics = driver.find_element("xpath", '/html/body/div[3]/div[2]/div[2]/div[3]/div[2]/aside/div/ul/li[1]/a').click()
    # quiz_statistics = driver.find_element("xpath", '//*[@id="sidebar_content"]/ul/li[1]/a').click()
    time.sleep(3)
    # try to see if the instructor has quiz statistics
    try:
      # try finding summary statistics if report already generated
      try:
        student_analysis = driver.find_element("xpath", '//*[@id="summary-statistics"]/header/div/div[2]/div/a/span[2]').click()
        # if report hasn't been generated yet, click button and wait for report to generate
      except:
        student_analysis = driver.find_element("xpath", '//*[@id="summary-statistics"]/header/div/div[2]/div/button').click()
        time.sleep(60)
    except:
      no_stats.append(i)
      # print("Does not have quiz statistics")
    time.sleep(5)

print("\n\n")
print("Instructor indices with no statistics:")
print(no_stats)
print("\nScript Complete!")

# Close the driver
driver.close()