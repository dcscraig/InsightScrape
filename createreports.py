import pandas as pd
import os
import os.path
from pathlib import Path

from coursereport import CourseReport


# will create reports for all subjects in
# current courses and save them in report folder
report_folder = Path("Output/Reports")

cur_year = 2024
#summaryfolder filenames are Summarylevelstage
summary_folder =  Path("downloads/schoolsum")
#ccv filenames are CCVLevelStage
ccv_folder =  Path("downloads/ccv")
#gender filenames
gender_folder =  Path("downloads/gender")
#asn filenames are course-level-1
asn_folder =  Path("downloads/asn")
# simd filenames are coursecode-level-simdlevel i.e C833-76-2
simd_folder =  Path("downloads/simd")

def get_ccv(folder,filename):
	filename = folder/(filename+".csv")
	if (os.path.isfile(filename)):
		data = pd.read_csv(filename, index_col=None)
		print(filename)
		print (data)
		data["Year"] = data["Year"].str[-2:]
		data["sig"] = data["Significant at 95% Confidence Level?"]
		data["ccv"] = data["Course Comparator Value"]
		data = data[data["Year"]==str(int(cur_year))[2:]]
		print(str(int(cur_year))[2:])
		data = data.drop(columns=["Unnamed: 7"])
		data = data.set_index(data["Course"])
	
	else:
		data = None
	return data


def get_gender_file(fname):
	data = None
	
	if (os.path.isfile(fname)):
		data = pd.read_csv(fname, index_col=None)
		data = data[data["Year"]==cur_year]
		data.drop(columns=["Unnamed: 13"])
	else:
		print ("no data")
	return data

def get_gender(folder,filename):
# 	filename = "downloads/gender/"+filename+".csv"
	
	final = {}
	m_fname = folder/(filename+"-1.csv")
	f_fname = folder/(filename+"-2.csv")
	final["male"] = get_gender_file(m_fname)
	final["female"] = get_gender_file(f_fname)
	return final
	
def get_simd_file(fname):
	data = None
	
	if (os.path.isfile(fname)):
		data = pd.read_csv(fname, index_col=None)
		data = data[data["Year"]==cur_year]
		data.drop(columns=["Unnamed: 13"])
	else:
		print ("no data")
	return data

	
def get_simd(folder,filename):
# 	filename = "downloads/gender/"+filename+".csv"
	final = {}
	for i in range(1,6):
		fname = folder/(filename+"-"+str(i)+".csv")
		final[i] = get_simd_file(fname)
	return final
	

	
def get_asn_file(fname):
	data = None
	if (os.path.isfile(fname)):
		data = pd.read_csv(fname, index_col=None)
		data = data[data["Year"]==cur_year]
		data.drop(columns=["Unnamed: 13"])
	else:
		print ("no data")
	return data

	
def get_asn(folder,filename):
# 	filename = "downloads/asn/"+filename+".csv"
	fname = folder/(filename+"-1"+".csv")
	return get_asn_file(fname)
	
	
	
	



def get_summary(folder,filename):
	filename = folder/(filename+".csv")
	print (filename)
	if (os.path.isfile(filename)):
		data = pd.read_csv(filename, index_col=None)
		data["Course Code"] = data['More Detail'].str[-4:]
		data = data.drop(columns=['More Detail',"Unnamed: 21"])
		data = data.set_index("Course Code")
	else:
		data = None
	
	
	return data


data = pd.read_csv("current_courses.csv", index_col=None)


levels = [75,76,77]
stages = ["S4","S5","S6"]
stages_num = ["1","2","3"]


summary_data = {}
ccv_data = {}

for level in levels:
	sum_temp = {}
	ccv_temp = {}
	index = 0
	for stage in stages:
		sum_temp[stage] = get_summary(summary_folder,"Summary"+str(level)+stages_num[index]) 
		ccv_temp[stage] = get_ccv(ccv_folder,"CCV"+str(level)+stages_num[index]) 
		index +=1
	summary_data[level] = sum_temp
	ccv_data[level] = ccv_temp
	
# 	summary_data[level] = temp
	



for index, row in data.iterrows():
	level = row["Level"]
	course_code = row["Course"]
	course_name = row["Course Title"]
	
	# 	course code-level-gender

	gender = get_gender(gender_folder,course_code+"-"+str(level))
	simd = get_simd(simd_folder,course_code+"-"+str(level))
	asn = get_asn(asn_folder,course_code+"-"+str(level))
	
	
	school_cols = ['Total','Resulted Entries % of Base Cohort','% Grade A','% Grades A to B','% Grades A to C','% Grades A to D','% No Award']
	national_cols = ['National % Grade A','National % Grades A to B','National % Grades A to C', 'National % Grades A to D', 'National % No Award']
	
	stages = ["S4","S5","S6"]
	full_summary = {}
	full_attainment = {}
			
	for stage in stages:
		full_summary[stage] = None
		full_attainment[stage] = None
		
		if (isinstance(summary_data[level][stage], pd.DataFrame)):
			temp = summary_data[level][stage][summary_data[level][stage]["Qualification Name"]==course_name].copy(deep=True)
			school = None
			national = None
			if (isinstance(temp, pd.DataFrame) and (course_code in temp.index)):
				if (not(isinstance(ccv_data[level][stage],pd.DataFrame))):
	# 				No ccv data for this level and stage
					temp_ccv = None
				else:
					temp_ccv = ccv_data[level][stage][ccv_data[level][stage]["Course"]==course_name]
			
				total = (temp['# Grades A to D'].values[0]+temp['# No Award'].values[0])
			
				temp["Total"] =total
		
				school = temp[school_cols]
				national = temp[national_cols]
			
				full_summary[stage] = {"school":school, "national":national}
			
			
				full_attainment[stage] = temp_ccv 
			else:
				print ("NOT FOUND ",stage)
	
	template = "final_template.docx"
	print (course_name)
	print (level)
	temp = CourseReport(template,Path("Output/Reports/"),full_summary,full_attainment,course_name,level,gender,simd,asn)
	
	