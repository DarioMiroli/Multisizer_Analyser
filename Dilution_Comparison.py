from MultisizerReader import MultiSizerReader
import os


#Get all spread sheet files in fodler and create multisizer files for each
folder = "./Data_Organised/Dilution_Comparisons"
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



MultiSizerReader.plotData(data,groupValues=ODs,logAxis=False,labels=labels,legend=False,title="Dilution comparison",xLims=(0.4,5))

combinedData,combinedTypes,combinedLabels = MultiSizerReader.sumByGroup(data,ODs,labels)
MultiSizerReader.plotData(combinedData,combinedTypes,labels=combinedLabels,logAxis=False,legend=False,
title="Dilution comparison",logNormalFits=False,xLims=(0.4,5))

MultiSizerReader.boxPlotData(combinedData,groupValues=combinedTypes,labels=combinedLabels,title="Dilution comparison")
