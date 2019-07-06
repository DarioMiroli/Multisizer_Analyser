import os
from MultisizerReader import MultiSizerReader
import matplotlib
import matplotlib.pyplot as plt

#Get all spread sheet files in fodler and create multisizer files for each
folder = "./Data_Organised/MG1655_600mMNaCl_Curve"
allFiles = os.listdir(folder)
multiSizerFiles = [allFiles[i] for i in range(len(allFiles)) if allFiles[i].endswith(".XLS")]
data = []
for files in multiSizerFiles:
    data.append(MultiSizerReader(path=os.path.join(folder,files)))

#Extract ODs from file names
ODList = []
labels = []
for i,d in enumerate(data):
    if d.name.split("_")[4] != "ON":
        ODList.append(float(d.name.split("_")[3] +"."+ d.name.split("_")[4]))
        labels.append("OD: {0} ".format(ODList[i]))
    else:
        ODList.append(100)
        labels.append("OD: ON ")

#************************ PLOT EVERYTHING **********************************
#Plotting all plots as individual traces
MultiSizerReader.plotData(data,ODList,labels=labels,legend=False,title="MG1655, 600mM NaCl growth curve",joymode= False)
#************************* Plot summed hists by OD *************************
combinedData,combinedODs,combinedLabels = MultiSizerReader.sumByGroup(data,ODList,labels)
MultiSizerReader.plotData(combinedData,combinedODs,labels=combinedLabels ,legend=True,alpha = 1.0,title = "MG1655, 600mM NaCl growth curve",joymode=False)
