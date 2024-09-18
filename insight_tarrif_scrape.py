import os
import time
import sys
import pickle
import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

import pandas as pd
import time,shutil
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
		
def createFolders():
	downloads = Path(os.getcwd()) / "downloads"
	folders = ["asn","ccv","gender","schoolsum","simd","tariff"]
	
	for folder in ["asn","gender","simd"]:
		os.makedirs(downloads/"tariff"/folder)
		
def clearDownloads():
	shutil.rmtree('downloads')



# temp folder for downloading from insight
# files are then moved to the correct folder
# located in downloads
download_folder = Path(os.getcwd()) / "tempDownloads/"

session_path = "selenium-session.pkl"
SELENIUM_URL = "http://127.0.0.1:51808"

# starts a seleneium session
# required chromedriver to be already running
SELENIUM_SESSION_PICKLE = "selenium-session.pkl"



tariff_overview_folder = Path("downloads/tariff") 
#folders to store the downloaded data
# simd filenames are coursecode-level-simdlevel i.e C833-76-2
simd_folder =  Path("downloads/tariff/simd")
#summary filenames are SummaryLevelStage i.e Summary751
# 75 N5, 76 Higher, 76 AH 
# 1-S4, 2-S5, 3-S6 
summary_folder =  Path("downloads/tariff/schoolsum")
#ccv filenames are CCVLevelStage
ccv_folder =  Path("downloads/tariff/ccv")
#gender filenames
gender_folder =  Path("downloads/tariff/gender")
#asn filenames are course-level-1
asn_folder =  Path("downloads/tariff/asn")


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


def processTable(table):
	data = {}
	for row in table.find_elements(By.CSS_SELECTOR,'tr')[1:]:
		cells = row.find_elements(By.TAG_NAME,'td')
		if(len(cells)==3):		
			area = cells[0].get_attribute("innerHTML").split("\n")[0]
			school = cells[1].get_attribute("innerHTML")
			vc = cells[2].get_attribute("innerHTML")
			
			if school[0]=="\n":
				school = -1
			else:
				school = float(school)
			if vc[0]=="\n":
				vc = -1
			else:
				vc = float(vc)
			data[area] = [school,vc]
	return data

def createTariffFile(data,fname):
	data = pd.DataFrame.from_dict(data)
	data = data.rename(index={0:"School",1:"VC"})
	data.to_csv(fname)
	return


def retrieveTariffOverview(browser,years,folder):
	#S4/S5/S6,S4,S5,S6,S5/S6
	#stage_group: 0,1,2,3,4,6
	stages = [0,1,2,3,5]
	stage_labels = ["All","S4","S5","S6","S5-S6"]
	# get all ccv data
	for year in years:
		for stage_index in range(len(stages)):
			keys = {"average":"ATS", "percentage":"RE","percentage2":"BCC"}
			for key in keys.values():	
				print(year, stage_index,key)
				url = "https://insight.scotxed.net/ca/a?Curricular+Areas+Year="+str(year)+"&Curricular+Areas+Data+To+Display="+key+"&Curricular+Areas+Top+Level+SCQF+Level=0&stage_group="+str(stages[stage_index])
				browser.get(url)
				table = browser.find_element(By.CSS_SELECTOR,"table[data-group]")
				fname = "tariff"+str(year)+str(stage_labels[stage_index])+key+".csv"
				fname =  folder / fname
				createTariffFile(processTable(table),fname)


def retrieveTariffwithSelector(browser,folder,selector,years):
	#S4/S5/S6,S4,S5,S6,S5/S6
	#stage_group: 0,1,2,3,4,6
	stages = [0,1,2,3,5]
	stage_labels = ["All","S4","S5","S6","S5-S6"]
	selector_url = selector["url"]
	selector_values = selector["values"]
	selector_labels = selector["labels"]
	
	for year in years:
		for stage_index in range(len(stages)):
			for selector_index in range(len(selector_values)):
				keys = {"average":"ATS", "percentage":"RE","percentage2":"BCC"}
				for key in keys.values():
					url = "https://insight.scotxed.net/ca/a?Curricular+Areas+Year="+str(year)+"&Curricular+Areas+Data+To+Display="+key+"&Curricular+Areas+Top+Level+SCQF+Level=0&stage_group="+str(stages[stage_index])+selector_url+"="+str(selector_values[selector_index])
					browser.get(url)
					table = browser.find_element(By.CSS_SELECTOR,"table[data-group]")
					fname = "tariff"+str(year)+str(stage_labels[stage_index])+str(selector_labels[selector_index])+key+".csv"
					fname =  folder / fname
					createTariffFile(processTable(table),fname)

def retrieveTariffGender(browser,years,folder):
	selector = {}
	selector["url"] = "&gender"
	selector["values"] = [1,2]
	selector["labels"] = ["Male","Female"]
	retrieveTariffwithSelector(browser,folder,selector,years)
	
def retrieveTariffASN(browser,years,folder):
	selector = {}
	selector["url"] = "&asn_group"
	selector["values"] = [1,2]
	selector["labels"] = ["ASN","NOASN"]
	retrieveTariffwithSelector(browser,folder,selector,years)

def retrieveTariffSIMD(browser,years,folder):
	selector = {}
	selector["url"] = "&simd_group"
	selector["values"] = [1,2,3,4,5]
	selector["labels"] = ["1","2","3","4","5"]
	retrieveTariffwithSelector(browser,folder,selector,years)
	
years = [2020,2021,2022,2023,2024]
retrieveTariffOverview(browser,years,tariff_overview_folder)
retrieveTariffGender(browser,years,tariff_overview_folder / "gender")
retrieveTariffASN(browser,years,tariff_overview_folder / "asn")
retrieveTariffSIMD(browser,years,tariff_overview_folder / "simd")

