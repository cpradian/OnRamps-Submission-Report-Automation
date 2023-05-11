def wait_for_file(directory, filename, timeout=300):
    import os
    import time

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


def rename_latest_file(directory, new_filename):
    import os

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


def canvas_scraper(driver_path, download_path, postlab_links_dir, lab_num):
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


    # specify the download directory
    download_path = download_path.replace("/", "\\")
    raw_download_path = r"{}".format(download_path)
    print(raw_download_path)

    options = EdgeOptions()

    options.use_chromium = True
    options.add_experimental_option("prefs", {
    # change download directory here:
    "download.default_directory": raw_download_path

    })

    # provide the path to the installed webdriver here:
    driver = webdriver.Edge(executable_path=driver_path, options=options)


    # read csv file to get list of links
    # provide path to csv file w/ links here:
    dataset = pd.read_csv(postlab_links_dir)

    # Grab only the column with the links and make an array
    lab = lab_num + " Link"
    urls = dataset[lab]

    instructors = dataset['Instructor']

    # this list will keep track of which instructors don't have quiz statistics
    no_stats = []

    # do log in process
    driver.get(urls[0])
    # allow 30 seconds to complete login process
    time.sleep(30) 

    for i in range(len(urls)):
        # Go to target page
        driver.get(urls[i])

        # Wait for 3 seconds to fully load
        time.sleep(3)

        # Locate the quiz statistics button and click
        quiz_statistics = driver.find_element("xpath", '/html/body/div[3]/div[2]/div[2]/div[3]/div[2]/aside/div/ul/li[1]/a').click()
        time.sleep(3)

        # try to see if the instructor has quiz statistics
        try:
        # try finding summary statistics if report already generated
            try:
                student_analysis = driver.find_element("xpath", '//*[@id="summary-statistics"]/header/div/div[2]/div/a/span[2]').click()
                time.sleep(1)
                new_name = instructors[i] + " " + lab_num + r" Quiz Student Analysis Report.csv"
                rename_latest_file(download_path, new_name)
            # if report hasn't been generated yet, click button and wait for report to generate
            except:
                student_analysis = driver.find_element("xpath", '//*[@id="summary-statistics"]/header/div/div[2]/div/button').click()
                old_name = lab_num + r" Quiz Student Analysis Report.csv"
                if wait_for_file(download_path, old_name):
                    new_name = instructors[i] + " " + lab_num + r" Quiz Student Analysis Report.csv"
                    rename_latest_file(download_path, new_name)
                else:
                    print(instructors[i] + " timed out. Did not download report")
        except:
            no_stats.append(i)
        
        time.sleep(5)

    print("\n\n")
    print("Instructor indices with no statistics:")
    for n in no_stats:
        print(instructors[n])
    print("\nScript Complete!")

    # Close the driver
    driver.close()
