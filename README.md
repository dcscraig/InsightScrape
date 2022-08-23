# Insight Scrape
This project is an automated attainment statistics generator for insight.scotxed.net. It is possibly only of interest to educators in secondary education in Scotland.

Insight is a great resource for Secondary Scottish teachers to gain knowledge about how well their students have attained in their SQA courses. One issue, however, is that to get to some of the data there are multilple buttons and pages to navigate to collate the data to do comparisons. Some examples of questions I want to answer are "How did students in my subject attain given their SIMD?" or "Is there a gender based attainment gap in your subject" or even "How well do students with ASN attain in your subject compared to Local and National?" My approach with these programs is to minimise the time required to collate attainment data in order to maximise the time spent analysing it and finding methods to improve attainment. I hate having to navigate a website with multiple clicks to get to thhe data I need, especially when I need to do it for multiple levels and subjects. 

The scripts are able to generate reports such as the ones shown below:

<img src="https://github.com/dcscraig/InsightScrape/blob/main/reportpage1.png" width="800">
<img src="https://github.com/dcscraig/InsightScrape/blob/main/reportpage2.png" width="800">


# Requirements

Python3, Pandas, Numpy, Seaborne. Install Anaconda (https://www.anaconda.com/). To get the data from insight: selenium and chromedriver. To generate reports: python-docx. You will obviously need a login to insight and access to an educational establishment's data.

# Main Scripts 

## insight_scrape.py 
Chromedriver needs to be running and once you run this script a window will appear with the insight homepage. Sign in using your usual approach (seemis login has been tested). Once you are at your school's homepage the script will start to automatically navigate to pages it needs and download the data. For an entire school's subjects it can take quite a while to get the data. I recomend leaving it alone and go for a cup of tea. All the data is stored in the downloads folder.

## createreports.py
This script will generate reports filling in all the required data ready for you to provide some commentary and next steps. 
# Usage
You will need to modify the current_courses file to match the courses that you wish to generate reports for.

1. run chromedriver
2. python insight_scrape.py 
3. python createreports.py

A word document for each subject and level with all the data provided will be placed in the reports folder.

# Technical
I have tried to comment the code to help understanding but the current documentation level leaves a lot to be desired. The report generation is a bit of a hack. If you have your own template and need some help please get in touch.

## Authors
* **Craig Stewart** - *Initial work* - (https://github.com/dcscraig)
## License

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">GoggleClips</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/dcscraig/GoggleClips" property="cc:attributionName" rel="cc:attributionURL">Craig Stewart</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/dcscraig/SchoolDataAnalysis" rel="dct:source">https://github.com/dcscraig/SchoolDataAnalysis</a>.
