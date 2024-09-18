from asyncio.subprocess import SubprocessStreamProtocol
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


#historic all

from pathlib import Path

def makeOverallGraphs():
    base = Path("downloads/tariff")
    selections = ["ALL","S4","S5","S6","S5-S6"]
    # years = [2017,2018,2019,2020,2021,2022]
    years = [2019,2020,2021,2022,2023]
    
    
    with PdfPages("Tariff Difference.pdf") as pdf:
        
        for sel in selections:
            title = sel+" Average Tariff Diff from VC"
            raw_data = []
            for year in years:
                year = str(year)
                temp = pd.read_csv(base/("tariff"+year+sel+"ATS.csv"))
                temp = temp.set_index("Unnamed: 0")
                temp = temp.loc["School"]-temp.loc["VC"]
                # temp = temp.loc["School"]
                temp = temp.rename(year)
                raw_data.append(temp)
               
            score = pd.concat(raw_data,axis=1)
            score = score.transpose()

            raw_data = []
            for year in years:
                year = str(year)
                temp = pd.read_csv(base/("tariff"+year+sel+"RE.csv"))
                temp = temp.set_index("Unnamed: 0")
                temp = temp.loc["School"]
                temp.name = year
                raw_data.append(temp)
            
            percent = pd.concat(raw_data,axis=1)
            percent = percent.transpose()
            
            score = score.drop(columns=["Religious and Moral Education","Wider Achievement"])
            percent = percent.drop(columns=["Religious and Moral Education","Wider Achievement"])
            print(percent["Technologies"])
            print(score["Technologies"])
            makeGraph(score,percent,title)
            pdf.savefig()
            plt.close()
    with PdfPages("Tariff Raw.pdf") as pdf:
        for sel in selections:
            title = sel+" Average Tariff"
            raw_data = []

            for year in years:
                year = str(year)
                temp = pd.read_csv(base/("tariff"+year+sel+"ATS.csv"))
                temp = temp.set_index("Unnamed: 0")
                # temp = temp.loc["School"]-temp.loc["VC"]
                temp = temp.loc["School"]
                temp.name = year
                raw_data.append(temp)
            
            score = pd.concat(raw_data,axis=1)
            score = score.transpose()
            
            raw_data = []
            for year in years:
                year = str(year)
                temp = pd.read_csv(base/("tariff"+year+sel+"RE.csv"))
                temp = temp.set_index("Unnamed: 0")
                # temp = temp.loc["School"]-temp.loc["VC"]
                temp = temp.loc["School"]
                temp.name = year
                raw_data.append(temp)
            
            percent = pd.concat(raw_data,axis=1)
            percent = percent.transpose()
            score = score.drop(columns=["Religious and Moral Education","Wider Achievement"])
            percent = percent.drop(columns=["Religious and Moral Education","Wider Achievement"])
            
            makeGraph(score,percent,title)
            pdf.savefig()
            plt.close()


def makeGraph(score,percent,title):
    fig, ax = plt.subplots(figsize=[11.69,8.27])
    fig.tight_layout()
    labels = score.columns.to_list()
    ax.plot(score,label=(score.columns))
    temp = ""
    for area in labels:
        temp = ax.scatter([0,1,2,3,4],score[area],s=40*percent[area],alpha=0.6)
    
    ax.set_title(title)
    temp = ax.legend(labels,loc="lower right")
    ax.add_artist(temp)

    from matplotlib.lines import Line2D
    custom_lines = []
    custom_lines.append(Line2D([0], [0], color=(0,0,0,0.6), lw=1, marker= "o",markersize=40*0.5))
    custom_lines.append(Line2D([0], [0], color=(0,0,0,0.6), lw=1, marker= "o",markersize=40*0.1))

    temp = ax.legend(custom_lines, ["50% of Entries","10% of Entries"])
    temp.set_title("% of School Entries")


# def makeOverallASNGraphs():
#     base = Path("downloads/tariff/asn")
#     selections = ["S4","S5","S6","S5-S6","All"]
#     years = [2017,2018,2019,2020,2021]
#     with PdfPages("ASN Tariff Difference.pdf") as pdf:
        
#         for sel in selections:
#             title = sel+" Average Tariff Diff from VC"
#             raw_data = []
#             for year in years:
#                 year = str(year)
#                 temp = pd.read_csv(base/("tariff"+year+sel+"ASN"+".csv"))
#                 temp = temp.set_index("Unnamed: 0")
#                 temp = temp.loc["School"]-temp.loc["VC"]
#                 # temp = temp.loc["School"]
#                 temp = temp.rename(year)
#                 raw_data.append(temp)
#                 print(temp)

#             data = pd.concat(raw_data,axis=1)

#             data = data.transpose()

#             plt.figure(figsize=(11.69,8.27))
#             plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
#             labels = data.columns.to_list()
#             print(data["Technologies"])
#             plt.plot(data["Technologies"],label=("Technologies"))
#             # plt.plot(data,label=(data.columns))
            
#             # data.plot.line()
#             plt.title(title)
#             # plt.legend(labels,loc="lower right")
#             pdf.savefig()
#             plt.close()
     

makeOverallGraphs()
# makeOverallASNGraphs()
