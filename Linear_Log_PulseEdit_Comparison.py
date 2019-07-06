from MultisizerReader import MultiSizerReader
import os


#Get all spread sheet files in fodler and create multisizer files for each
folder = "./Data_Organised/Linear_Log_PulseEdit_Comparison"
allFiles = os.listdir(folder)
multiSizerFiles = [allFiles[i] for i in range(len(allFiles)) if allFiles[i].endswith(".XLS")]
data = []
for files in multiSizerFiles:
    data.append(MultiSizerReader(path=os.path.join(folder,files)))

#split files into YD133 and YD133 + PWR20
cellType = []
labels = []
for d in data:
    if d.name.split("_")[5] == "linear":
        labels.append("linear + pulse edit ")
        cellType.append(0)
    if d.name.split("_")[5] == "LOG":
        labels.append("Log + pulse edit ")
        cellType.append(2)
    if d.name.split("_")[5] == "LOGNOPE":
        labels.append("Log - pulse edit")
        cellType.append(3)
    if d.name.split("_")[5] == "NOPE":
        labels.append("Linear - pulse edit ")
        cellType.append(1)


MultiSizerReader.plotData(data,groupValues=cellType,logAxis=False,labels=labels,spacing=0.02,legend=True,
        title="Linear, Log and pulse edit comparsion",xLims=(0.3,5), logNormalFits=True)

#combinedData,combinedTypes,combinedLabels = MultiSizerReader.sumByGroup(data,cellType,labels)
#MultiSizerReader.plotData(combinedData,combinedTypes,labels=combinedLabels,logAxis=False,legend=True,
#        title="All strain comparison (averaged)",logNormalFits=False,xLims=(0.3,5))
