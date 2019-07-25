from MultisizerReader import MultiSizerReader
import os
import matplotlib.pyplot as plt

#Get all spread sheet files in fodler and create multisizer files for each
folder = "./Data_Organised/DilutionTestingLowOD"
allFiles = os.listdir(folder)
multiSizerFiles = [allFiles[i] for i in range(len(allFiles)) if allFiles[i].endswith(".XLS")]
data = []
for files in multiSizerFiles:
    data.append(MultiSizerReader(path=os.path.join(folder,files)))

#split files into YD133 and YD133 + PWR20
ODs = []
labels = []
dilutions =[]
for d in data:
    OD = d.name.split("_")[4] + "." + d.name.split("_")[5]
    if d.name.split("_")[2] == "5":
        dilutions.append("$10^5$")
        labels.append("$10^5$ OD: {}".format(OD))
    if d.name.split("_")[2] == "7":
        dilutions.append("$10^7$")
        labels.append("$10^7$ OD: {}".format(OD))
    ODs.append(float(OD))

fig, ax = plt.subplots(nrows=1,ncols=2,figsize=(14,9))

combinedData,combinedTypes,combinedLabels = MultiSizerReader.sumByGroup(data,ODs,labels)
MultiSizerReader.plotData(combinedData,combinedTypes,labels=combinedLabels,logAxis=False,legend=True,title="OD ~ 0.05",logNormalFits=False,xLims=(0.4,4),colorScale=False,smoothing=5,showStats=False,ax=ax[0],text=False,cbarLabel="$\mathbf{OD_{600}}$")

#Get all spread sheet files in fodler and create multisizer files for each
folder = "./Data_Organised/DilutionTestingHighOD"
allFiles = os.listdir(folder)
multiSizerFiles = [allFiles[i] for i in range(len(allFiles)) if allFiles[i].endswith(".XLS")]
data = []
for files in multiSizerFiles:
    data.append(MultiSizerReader(path=os.path.join(folder,files)))

#split files into YD133 and YD133 + PWR20
ODs = []
labels = []
dilutions =[]
for d in data:
    OD = d.name.split("_")[4] + "." + d.name.split("_")[5]
    if d.name.split("_")[2] == "5":
        dilutions.append("$10^5$")
        labels.append("$10^5$ OD: {}".format(OD))
    if d.name.split("_")[2] == "7":
        dilutions.append("$10^7$")
        labels.append("$10^7$ OD: {}".format(OD))
    ODs.append(float(OD))




combinedData,combinedTypes,combinedLabels = MultiSizerReader.sumByGroup(data,ODs,labels)
MultiSizerReader.plotData(combinedData,combinedTypes,labels=combinedLabels,logAxis=False,legend=True,title="OD ~ 0.2",logNormalFits=False,xLims=(0.4,4),colorScale=False,smoothing=5,showStats=False,ax=ax[1],text=False,cbarLabel="$\mathbf{OD_{600}}$")









ax[0].text(0.03, 0.93 , "A", transform=ax[0].transAxes, size=35, weight='bold',color="k")
ax[1].text(0.03, 0.93 , "B", transform=ax[1].transAxes, size=35, weight='bold',color="k")
ax[0].legend(fontsize="xx-large")
ax[1].legend(fontsize="xx-large")
fig.tight_layout()
plt.show()
