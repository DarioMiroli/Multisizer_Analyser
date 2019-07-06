import os
from MultisizerReader import MultiSizerReader
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

#DELETE DOES NTO BELONG HERE LIKE AT ALL
#plt.errorbar([0,200,600],[36,44,104],yerr=[1,1,3],fmt="--o",ecolor='k',capsize=3)
plt.plot([0,200,400,600],[2.134,2.122,1.674,0.981],'--o')
plt.xlabel("NaCl Concentration (mM)")
plt.ylabel("Average genomes/cell")
plt.tight_layout()
plt.show()

#exit()

#Get all spread sheet files in fodler and create multisizer files for each
folders = [ "./Data_Organised/YD133+PWR20_000_GrowthCurve","./Data_Organised/YD133+PWR20_200_GrowthCurve",
             "./Data_Organised/YD133+PWR20_400_GrowthCurve","./Data_Organised/YD133+PWR20_600_GrowthCurve/All"]
concentrations = ["0","200","400","600"]
dataDic = {}
for i,folder in enumerate(folders):
    allFiles = os.listdir(folder)
    multiSizerFiles = [allFiles[i] for i in range(len(allFiles)) if allFiles[i].endswith(".XLS")]
    data = []
    for files in multiSizerFiles:
        data.append(MultiSizerReader(path=os.path.join(folder,files)))
    dataDic[concentrations[i]] = data


combinedDataDic = {}
titles = ["0mM NaCl","200mM NaCl","400mM NaCl","600mM NaCl"]
for i,key in enumerate(concentrations):
    data = dataDic[key]
    ODList = [float(data[i].name.split("_")[3] + "." + data[i].name.split("_")[4]) for i in range(len(data)) ]
    #Inspect all individual traces
    #MultiSizerReader.plotData(dataDic[key],ODList,ODList,legend=False,logAxis=False,xLims=(0.4,5),title=key,joymode= False)
    combinedData,combinedODs = MultiSizerReader.sumByGroup(data,ODList)
    for j,d in enumerate(combinedData): d.OD = combinedODs[j]

    combinedDataDic[key] = combinedData
    labels = ["OD: {} ".format(k) for k in combinedODs]
    #Inspect collected traces
    #MultiSizerReader.plotData(combinedData,combinedODs,labels,legend=False,logAxis=False,xLims=(0.4,5),title=titles[i],joymode= False)

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


ODs = [0.059,0.063,0.059,0.048]
comparisonData = []
labels = []
concs = []
means = []
for i in range(len(ODs)):
    print(type(combinedDataDic[concentrations[i]]))
    for d in combinedDataDic[concentrations[i]]:
        if d.OD == ODs[i]:
            comparisonData.append(d)
            labels.append("{} mM NaCl".format(concentrations[i]))
            concs.append(concentrations[i])
            means.append(d.getMean())
MultiSizerReader.plotData(comparisonData,labels=labels,legend=False,logAxis=False,xLims=(0.4,5),title="Osmo comparison OD ~0.06",joymode= False)
MultiSizerReader.boxPlotData(comparisonData,labels=concentrations,title="Osmo comparison OD ~0.06",positions=[0.0,2.0,4.0,6.0])

plt.plot(concs,means,"--o")
plt.xlabel("NaCl Concentration (mM)")
plt.ylabel("Mean cell volume $\mu m^3$")
plt.tight_layout()
plt.show()



exit()
