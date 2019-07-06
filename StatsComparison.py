from MultisizerReader import MultiSizerReader
import os

#Get all spread sheet files in fodler and create multisizer files for each
folder = "./Data_Organised/Stats_Test"

allFiles = os.listdir(folder)
multiSizerFiles = [allFiles[i] for i in range(len(allFiles)) if allFiles[i].endswith(".XLS")]
data = []
for files in multiSizerFiles:
    data.append(MultiSizerReader(path=os.path.join(folder,files)))
#Extract ODs from file names
groupList = [float(d.name.split("_")[5]) for d in data]

#************************ PLOT EVERYTHING **********************************
#Plotting all plots as individual traces

for currentCount in [200000]:
    countData = []
    countGroup = []
    for i in range(len(data)):
        if groupList[i] == currentCount:
            countData.append(data[i])
            countGroup.append(groupList[i])
    MultiSizerReader.plotData(countData,[j for j in range(len(countData))],logAxis=False,smoothing=1 ,spacing=0.025,xLims=(0,5),
                                labels=["Count: {0} ".format(countGroup[k]) for k in range(len(countGroup))],legend=False,
                                title="BW25113 200k cells",joymode= False,logNormalFits=True)

#************************* Plot summed hists by OD *************************
#combinedData,combinedODs = MultiSizerReader.sumByGroup(data,ODList)
#MultiSizerReader.plotData(combinedData,combinedODs,labels=["OD: {0} ".format(combinedODs[i]) for i in range(len(combinedODs))],legend=True,alpha = 1.0,title = "MG1655 Summed cell size growth curve",joymode=False)
