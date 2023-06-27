# import required modules
import pandas as pd
import os
import glob

# renaming function that takes in directory and list of instructors
def rename(directory, instructors):
    os.chdir(directory)
    num = 0
    for file in [file for file in sorted(os.listdir(), key=os.path.getmtime)]:
        # choose appropriate number for Post-Lab naming:
        os.rename(file, instructors[num] + r" Post-Lab 3 Quiz Student Analysis Report.csv")
        num += 1

# read the csv files with links to canvas pages
dataset = pd.read_csv(r"C:\Users\Calvin Pradian\Documents\OnRamps\Gather Links Instructions\Post-Lab Links.csv")

# copy and paste the no_stats list here
no_stats = [171]

# grab college course column from csv file
college_course = dataset["Instructor"]
instructors = []

# converts pandas dataset to array
for course in college_course:
    instructors.append(course)

print (instructors[171])
# this loop will remove the instructors with no stats from the renaming process

for i in range(len(no_stats)):
    del instructors[no_stats[i]]
    try:
        no_stats[i+1] = no_stats[i+1] - 1
    except:
        print("All no stats removed!")

# provide path to folder to be renamed
rename(r"C:\Users\Calvin Pradian\Box\22-23 PHY Student Graders\PHY 22-23 Lab Submission Reports\Lab 3 Test", instructors)

print('Renaming Completed!')

