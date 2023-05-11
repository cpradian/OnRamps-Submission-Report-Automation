# Function to run gather links webscraper

def run_gather_links(webdriver_path, general_links_path):
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


    # specify  options

    options = EdgeOptions()
    options.use_chromium = True

    # provide the path to the installed webdriver here:
    driver = webdriver.Edge(executable_path=webdriver_path)


    # read csv file to get list of general links
    # provide path to csv file w/ links here:
    dataset = pd.read_csv(general_links_path)

    # Grab the course instructor names and urls and put them into arrays
    instructors = dataset["Instructor"]
    urls = dataset["Links"]

    # Initialize empty arrays for the links for each of the Post-Labs
    post_lab1_links = []
    post_lab2_links = []
    post_lab3_links = []
    post_lab4_links = []
    post_lab5_links = []
    post_lab6_links = []
    post_lab7_links = []
    post_lab8_links = []

    # do log in process
    driver.get(urls[0])
    # allow 30 seconds to complete login process
    time.sleep(30) 

    for i in range(len(urls)):
        print(instructors[i])
        # Go to target page
        driver.get(urls[i])
        # Wait for 5 seconds to fully load
        time.sleep(3)
        # Locate the Quizzes button and click
        quizzes = driver.find_element("xpath", '//*[@id="section-tabs"]/li[8]/a').click()
        time.sleep(3)

        # Extract Post-Lab 1 Links
        element = driver.find_element("xpath", "// a[contains(text(),\'Post-Lab 1')]")
        post_lab_link = element.get_attribute('href')
        post_lab1_links.append(post_lab_link)

        # Extract Post-Lab 2 Links
        element = driver.find_element("xpath", "// a[contains(text(),\'Post-Lab 2')]")
        post_lab_link = element.get_attribute('href')
        post_lab2_links.append(post_lab_link)

        # Extract Post-Lab 3 Links
        element = driver.find_element("xpath", "// a[contains(text(),\'Post-Lab 3')]")
        post_lab_link = element.get_attribute('href')
        post_lab3_links.append(post_lab_link)

        # Extract Post-Lab 4 Links
        element = driver.find_element("xpath", "// a[contains(text(),\'Post-Lab 4')]")
        post_lab_link = element.get_attribute('href')
        post_lab4_links.append(post_lab_link)

        # Extract Post-Lab 5 Links
        element = driver.find_element("xpath", "// a[contains(text(),\'Post-Lab 5')]")
        post_lab_link = element.get_attribute('href')
        post_lab5_links.append(post_lab_link)

        # Extract Post-Lab 6 Links
        element = driver.find_element("xpath", "// a[contains(text(),\'Post-Lab 6')]")
        post_lab_link = element.get_attribute('href')
        post_lab6_links.append(post_lab_link)

        # Extract Post-Lab 7 Links
        element = driver.find_element("xpath", "// a[contains(text(),\'Post-Lab 7')]")
        post_lab_link = element.get_attribute('href')
        post_lab7_links.append(post_lab_link)

        # Extract Post-Lab 8 Links
        element = driver.find_element("xpath", "// a[contains(text(),\'Post-Lab 8')]")
        post_lab_link = element.get_attribute('href')
        post_lab8_links.append(post_lab_link)

        time.sleep(1)

    # Convert gathered data to csv file
    finished = pd.DataFrame({'Instructor': instructors,
                            'Post-Lab 1 Link': post_lab1_links,
                            'Post-Lab 2 Link': post_lab2_links,
                            'Post-Lab 3 Link': post_lab3_links,
                            'Post-Lab 4 Link': post_lab4_links,
                            'Post-Lab 5 Link': post_lab5_links,
                            'Post-Lab 6 Link': post_lab6_links,
                            'Post-Lab 7 Link': post_lab7_links,
                            'Post-Lab 8 Link': post_lab8_links
                            })
    finished.to_csv("Post-Lab Links New.csv", index=False)

    # Close the driver
    driver.close()