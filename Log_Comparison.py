from MultisizerReader import MultiSizerReader
import os

#Get all spread sheet files in fodler and create multisizer files for each
folder = "./Data_Organised/Log_Comparison"
allFiles = os.listdir(folder)
multiSizerFiles = [allFiles[i] for i in range(len(allFiles)) if allFiles[i].endswith(".XLS")]
data = []
for files in multiSizerFiles:
    data.append(MultiSizerReader(path=os.path.join(folder,files)))
#Extract ODs from file names
groupList = [(d.name) for d in data]

#************************ PLOT EVERYTHING **********************************
#Plotting all plots as individual traces
labels = ["Linear PE ","Linear ","Log "]
#data = [data[0]]
#labels = [labels[0]]
MultiSizerReader.plotData(data,labels=labels,logAxis=False,smoothing=15 ,spacing=0.025,xLims=(0,10),
        legend=False,title="Log vs Linear Comparison",joymode= False,logNormalFits=True)

#************************* Plot summed hists by OD *************************
#combinedData,combinedODs = MultiSizerReader.sumByGroup(data,ODList)
#MultiSizerReader.plotData(combinedData,combinedODs,labels=["OD: {0} ".format(combinedODs[i]) for i in range(len(combinedODs))],legend=True,alpha = 1.0,title = "MG1655 Summed cell size growth curve",joymode=False)
