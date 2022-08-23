import os
import time
import sys
import pickle
import os
from pathlib import Path



from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException

import time,shutil
import pandas as pd
import time

#url details
# options insight url
# year=2019
# QualLevel=75,76,77
# age_group=0
# asn_group=0
# eal_group=0
# ethnicity=0
# gender=0
# highest_scqf_course_to_date=0
# lac_group=0
# leaver_destination_group=0
# pupil_points_group=0
# simd_group=0
# stage_group=0 (S4,S5,S6: 1,2,3 )





# attach to a webdriver to control website
class PersistentRemote(webdriver.Remote):
    def __init__(self,op,session_id=None):
        super(PersistentRemote, self).__init__(
            options=op,command_executor=SELENIUM_URL,
            desired_capabilities=DesiredCapabilities.CHROME,
        )
        #
        # This will create a new window.
        if session_id is not None:
            # Close new window.
            self.close()
            # Change to other session.
            self.session_id = session_id
            # Will raise WebDriverException if session no longer valid.
            try:
                self.title
            except WebDriverException:
                raise WebDriverException(f"Session '{session_id}' no longer valid.")

#simple class to handle the downloading of the tabular data
#for the given url
class InsightDownload:

	def	__init__(self,browser,folder,download_folder):
		self.broswer = browser
		self.download_folder = download_folder
		self.folder = folder
	
	def getFile(self,fname,url,not_found_msg):
		if(not(os.path.isfile(self.folder/fname))):
			browser.get(url)
			temp = browser.find_elements_by_link_text("Download Data")
			if (len(temp)==0):
				print(not_found_msg)
			else:
				temp[1].click()
				while( not os.path.exists(download_folder/"table.csv")):
					print("waiting on file")
					time.sleep(0.5)
				shutil.move(self.download_folder/"table.csv",self.folder/fname)
		else:
			print("already exists")





# retrieve CCV values for all subject in school
# for all the levels(N5,H,AH) and stages(S4,S5,S6)
def retrieveCCV(browser,ccvfolder,download_folder):
	levels = [75,76,77]
	stages = [1,2,3]
	year = "2021"
	# get all ccv data
	for level in levels:
		for stage in stages:
			url = "https://insight.scotxed.net/lccc/agc?Course+Comparison+Measure+All+Graded+Courses+Year="+year+"&Course+Comparison+Measure+All+Graded+Courses+Confidence+Level=95&Course+Comparison+Measure+All+Graded+Courses+Data+Provider=SQA&Course+Comparison+Measure+All+Graded+Courses+SQA+CN-HS+QualLevel="+str(level)+"&Course+Comparison+Measure+All+Graded+Courses+SQA+Product+Type=CN-HS&age_group=0&asn_group=0&eal_group=0&ethnicity=0&gender=0&highest_scqf_course_to_date=0&lac_group=0&leaver_destination_group=0&pupil_points_group=0&simd_group=0&stage_group="+str(stage) 
			browser.get(url)
			temp = browser.find_elements_by_link_text("Download Extended Data")
			if (len(temp)==0):
				print("No data for", level, stage)
			else:
				temp[0].click()
				while( not os.path.exists(download_folder/"table.csv")):
					time.sleep(0.5)
				fname = "CCV"+str(level)+str(stage)+".csv"
				shutil.move(download_folder/"table.csv",ccvfolder/fname)

# retrieve grade attainment for all subjects in school
# for all the levels(N5,H,AH) and stages(S4,S5,S6)
def retrieveAttainment(browser,year,summary_folder,download_folder):			
	levels = [75,76,77]
	stages = [1,2,3]
	for level in levels:
		for stage in stages:
			url = "https://insight.scotxed.net/wscs?Course+Summary+Measure+Year="+str(year)+"&Course+Summary+Measure+All+Courses+Data+Provider=SQA&Course+Summary+Measure+All+Courses+SQA+CN-HS+QualLevel="+str(level)+"&Course+Summary+Measure+All+Courses+SQA+Product+Type=CN-HS&gender=0&stage_group="+str(stage)
			browser.get(url)
			temp = browser.find_elements_by_link_text("Download Data")
			if (len(temp)==0):
				print("No data for", level, stage)
			else:
				temp[0].click()
				while( not os.path.exists(download_folder/"table.csv")):
					time.sleep(0.5)
				fname = "Summary"+str(level)+str(stage)+".csv"
				# move from the download folder into the summary folder
				shutil.move(download_folder/"table.csv",summary_folder/fname)

def retrieveSimdAll(browser,subjects,simd_folder,download_folder):
	num_subjects = len(subjects)
	# school_name = browser.find_elements_by_tag_name("button")[0].text
	downloader = InsightDownload(browser,simd_folder,download_folder)
	for index, subject in subjects.iterrows():
		print(subject["Course"],subject["Level"])
		print(index+1,((index+1)/num_subjects))
		retrieveSimdSubj(downloader,subject)
	

def retrieveSimdSubj(downloader,subject):	
	level = subject["Level"]
	course_code = subject["Course"]
	simds = [1,2,3,4,5]
	for simd in simds:
		fname = course_code+"-"+str(level)+"-"+str(simd)+".csv"
		url = "https://insight.scotxed.net/asgc/pre?Graded+Course+Measure+Data+Provider=SQA&Graded+Course+Measure+SQA+CN-HS+QualLevel="+str(level)+"&Graded+Course+Measure+SQA+Product+Type=CN-HS&Graded+Course+Measure+SQA+CN-HS+"+str(level)+"+Course="+course_code+"&age_group=0&asn_group=0&eal_group=0&ethnicity=0&gender=0&highest_scqf_course_to_date=0&lac_group=0&leaver_destination_group=0&pupil_points_group=0&simd_group="+str(simd)+"&stage_group=0"
		downloader.getFile(fname,url,"No data for "+str(level)+" "+str(simd))

def retrieveAttainmentbyGenderAll(browser,subjects,gender_folder,download_folder):
	num_subjects = len(subjects)
	downloader = InsightDownload(browser,gender_folder,download_folder)
	for index, subject in subjects.iterrows():
		print(subject["Course"],subject["Level"])
		print(index+1,((index+1)/num_subjects))
		retrieveAttainmentbySubjectGender(downloader,subject)

def retrieveAttainmentbySubjectGender(downloader,subject):
	level = subject["Level"]
	course_code = subject["Course"]
	genders = [1,2]
	for gender in genders:
		fname = course_code+"-"+str(level)+"-"+str(gender)+".csv"
		url = "https://insight.scotxed.net/asgc/pre?Graded+Course+Measure+Data+Provider=SQA&Graded+Course+Measure+SQA+CN-HS+QualLevel="+str(level)+"&Graded+Course+Measure+SQA+Product+Type=CN-HS&Graded+Course+Measure+SQA+CN-HS+"+str(level)+"+Course="+course_code+"&age_group=0&asn_group=0&eal_group=0&ethnicity=0&gender="+str(gender)+"&highest_scqf_course_to_date=0&lac_group=0&leaver_destination_group=0&pupil_points_group=0&simd_group=0&stage_group=0"
		downloader.getFile(fname,url,"No data for "+str(level)+" "+str(gender))
		
def retrieveAttainmentbyASN(browser,subjects,gender_folder,download_folder):
	num_subjects = len(subjects)
	downloader = InsightDownload(browser,gender_folder,download_folder)
	for index, subject in subjects.iterrows():
		print(subject["Course"],subject["Level"])
		print(index+1,((index+1)/num_subjects))
		retrieveAttainmentbySubjectASN(downloader,subject)

def retrieveAttainmentbySubjectASN(downloader,subject):
	level = subject["Level"]
	course_code = subject["Course"]
	asns = [1]
	for asn in asns:
		fname = course_code+"-"+str(level)+"-"+str(asn)+".csv"
		url = "https://insight.scotxed.net/asgc/pre?Graded+Course+Measure+Data+Provider=SQA&Graded+Course+Measure+SQA+CN-HS+QualLevel="+str(level)+"&Graded+Course+Measure+SQA+Product+Type=CN-HS&Graded+Course+Measure+SQA+CN-HS+"+str(level)+"+Course="+course_code+"&age_group=0&asn_group="+str(asn)+"&eal_group=0&ethnicity=0&gender=0&highest_scqf_course_to_date=0&lac_group=0&leaver_destination_group=0&pupil_points_group=0&simd_group=0&stage_group=0"
		print(course_code," ",level," ",asn)
		downloader.getFile(fname,url,"No data for "+str(level)+" ")
			
		
def createFolders():
	downloads = Path(os.getcwd()) / "downloads"
	folders = ["asn","ccv","gender","schoolsum","simd"]
	for folder in folders:
		os.makedirs(downloads/folder)
def clearDownloads():
	shutil.rmtree('downloads')


if (len(sys.argv)==2):
	if sys.argv[1]=="-clear":
		clearDownloads()
		createFolders()
		print("download folders cleared")
		exit()



# temp folder for downloading from insight
# files are then moved to the correct folder
# located in downloads
download_folder = Path(os.getcwd()) / "tempDownloads/"

session_path = "selenium-session.pkl"
SELENIUM_URL = "http://127.0.0.1:9515"

# starts a seleneium session
# required chromedriver to be already running
SELENIUM_SESSION_PICKLE = "selenium-session.pkl"


#folders to store the downloaded data
# simd filenames are coursecode-level-simdlevel i.e C833-76-2
simd_folder =  Path("downloads/simd")
#summary filenames are SummaryLevelStage i.e Summary751
# 75 N5, 76 Higher, 76 AH 
# 1-S4, 2-S5, 3-S6 
summary_folder =  Path("downloads/schoolsum")
#ccv filenames are CCVLevelStage
ccv_folder =  Path("downloads/ccv")
#gender filenames
gender_folder =  Path("downloads/gender")
#asn filenames are course-level-1
asn_folder =  Path("downloads/asn")


# custom options to move the download path to within
# the development folder
op = webdriver.ChromeOptions()
op.add_experimental_option("prefs",{'download.default_directory':str(download_folder),"download.directory_upgrade":True})
try:
	session = pickle.load(open(SELENIUM_SESSION_PICKLE, 'rb'))
	browser = PersistentRemote(op,session)
	# If you get to here then you are using an existing session.
except (FileNotFoundError, WebDriverException):
    # If you end up here then you are creating a new session.
    browser = PersistentRemote(op)
    pickle.dump(browser.session_id, open(SELENIUM_SESSION_PICKLE, 'wb'))
# try to access insight homepage
browser.get("https://insight.scotxed.net/")
print("Awaiting user login confirmation")
# rather than storing passwords with potential security issues 
# the script will wait until you are signed in and at the homepage 
# for the institution you have access to 
while(browser.current_url!="https://insight.scotxed.net/"):
	print(browser.current_url)
	print("Awaiting user to login to the insight dashboard")
	time.sleep(1)
print("Logged in")

year = 2021
startstart = time.time()
retrieveCCV(browser,ccv_folder,download_folder)
retrieveAttainment(browser,year,summary_folder,download_folder)

subjects = pd.read_csv("current_courses.csv", index_col=None)
print(subjects)
start = time.time()
retrieveSimdAll(browser,subjects,simd_folder,download_folder)
print("SIMD time: ",time.time()-start)

start = time.time()
retrieveAttainmentbyGenderAll(browser,subjects,gender_folder,download_folder)
print("Gender time: ",time.time()-start)

start = time.time()
retrieveAttainmentbyASN(browser,subjects,asn_folder,download_folder)
print("ASN time: ",time.time()-start)

print("TOTAL TIME ",time.time()-startstart)




