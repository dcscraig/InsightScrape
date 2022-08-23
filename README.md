# InsightScrape
Automated attainment statistics generator from insight.scotxed.net. Possibly only of interest to educators in secondary education in Scotland.


# School Data Analysis
Automated individual Scottish school data analysis for SQA results. 

# Requirements

Python3, Pandas, Numpy, Seaborne. Install Anaconda (https://www.anaconda.com/). To generate python-docx

# Usage

You will need to add your own school results file from your sqa coordinator. Name it the year you are analysing ie Data/SchoolResults/2022.xlsx .

python Overview.py will produce the overview pdfs of all the N5 subjects and Higher Subjects.

python resulttrends.py will produce the result trends pdfs of all the N5 subjects and Higher Subjects.

# Background

Insight (https://insight-guides.scotxed.net/stepbystep.htm) provides Scottish schools a variety of metrics to judge attainment. The release schedule for Insight is often several months after results day. It would be useful to have an overview of results as soon as they are released and for more in depth analysis of those results to be conducted.

# Requirements

All education establishments that use SQA courses will have a coordinator that can access results for the entire establishment. Most of the analysis included here will need those results in an Excel spreadsheet.

Grade boundaries, Component marks and national attainment is provided by the SQA Statistics and information (https://www.sqa.org.uk/sqa/78673.html). I have included the files that I have used with minor alterations. 

# Scripts
## Overview (Overview.py)


# Technical

I have tried to comment the code to help understanding but the current documentation level leaves a lot to be desired. Data access is handled through DataStore and makes use of a DataCache to reduce repeated file access. Not entirely convinced that this approach is conceptually that great but it works.


## Authors

* **Craig Stewart** - *Initial work* - (https://github.com/dcscraig)

## License

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">GoggleClips</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/dcscraig/GoggleClips" property="cc:attributionName" rel="cc:attributionURL">Craig Stewart</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/dcscraig/SchoolDataAnalysis" rel="dct:source">https://github.com/dcscraig/SchoolDataAnalysis</a>.
