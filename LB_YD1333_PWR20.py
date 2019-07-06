import os
from MultisizerReader import MultiSizerReader
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


#Get all spread sheet files in fodler and create multisizer files for each
folders = [ "./Data_Organised/LB_YD133_PWR20"]
concentrations = ["0"]
dataDic = {}
for i,folder in enumerate(folders):
    allFiles = os.listdir(folder)
    multiSizerFiles = [allFiles[i] for i in range(len(allFiles)) if allFiles[i].endswith(".XLS")]
    data = []
    for files in multiSizerFiles:
        data.append(MultiSizerReader(path=os.path.join(folder,files)))
    dataDic[concentrations[i]] = data


combinedDataDic = {}
titles = ["LB"]
for i,key in enumerate(concentrations):
    data = dataDic[key]
    ODList = [float(data[i].name.split("_")[3] + "." + data[i].name.split("_")[4]) for i in range(len(data)) ]
    #Inspect all individual traces
    MultiSizerReader.plotData(dataDic[key],ODList,ODList,legend=False,logAxis=False,xLims=(0.4,5),title=key,joymode= False)
    combinedData,combinedODs = MultiSizerReader.sumByGroup(data,ODList)
    for j,d in enumerate(combinedData): d.OD = combinedODs[j]

    combinedDataDic[key] = combinedData
    labels = ["OD: {} ".format(k) for k in combinedODs]
    #Inspect collected traces
    MultiSizerReader.plotData(combinedData,combinedODs,labels,legend=False,logAxis=False,xLims=(0.4,5),title=titles[i],joymode= False)

#Plot averages
for key in concentrations:
    condition = key
    dataList  =  combinedDataDic[key]
    ODs = [d.OD for d in dataList ]
    means = np.asarray([d.getMean() for d in dataList])
    modes = np.asarray([d.getMode() for d in dataList])
    stdevs = np.asarray([d.getStDev() for d in dataList])
    p = plt.plot(ODs,means,'o--',label=key+" mM NaCl")
    plt.fill_between(ODs,means+stdevs,means-stdevs,alpha=0.1)
    #plt.plot(ODs,modes,"*",c=p[0].get_color())
plt.xscale("log")
for item in ([plt.gcf().get_axes()[0].title,plt.gcf().get_axes()[0].xaxis.label, plt.gcf().get_axes()[0].yaxis.label]
    + plt.gcf().get_axes()[0].get_xticklabels() + plt.gcf().get_axes()[0].get_yticklabels()):
    item.set_fontsize(20)
plt.gcf().get_axes()[0].set_xticks([0.001,0.003,0.01,0.03,0.1,0.3,1,4])
plt.gcf().get_axes()[0].xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.gcf().set_size_inches(12, 8 )
plt.legend()
plt.xlabel("OD$_{600}$")
plt.ylabel("Mean cell volume $\mu m^3$")
plt.gcf().get_axes()[0].set_title("Cell size at high osmollarity",fontsize=20)
plt.gca().xaxis.grid(True)
plt.show()


ODs = [0.11]
comparisonData = []
labels = []
for i in range(len(ODs)):
    print(type(combinedDataDic[concentrations[i]]))
    for d in combinedDataDic[concentrations[i]]:
        if d.OD == ODs[i]:
            comparisonData.append(d)
            labels.append("{} mM NaCl".format(concentrations[i]))
MultiSizerReader.plotData(comparisonData,labels=labels,legend=False,logAxis=False,xLims=(0.4,5),title="Osmo comparison OD ~0.1",joymode= False)
MultiSizerReader.boxPlotData(comparisonData,labels=labels,title="Osmo comparison OD ~0.1")


exit()
