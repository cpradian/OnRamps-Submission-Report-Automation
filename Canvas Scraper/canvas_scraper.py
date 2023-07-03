# canvas_scraper.py

# import necessary libraries 
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

class CanvasScraper:
    def __init__(self, driver_path):

        options = EdgeOptions()
        options.use_chromium = True

        # provide the path to the installed webdriver here:
        self.driver = webdriver.Edge(executable_path=driver_path, options=options)
    
    def login(self, url):
        # navigate to a canvas webpage which will prompt login
        self.driver.get(url)
        # allow 30 seconds to complete login process
        time.sleep(30) 