from MultisizerReader import MultiSizerReader
import os


#Get all spread sheet files in fodler and create multisizer files for each
folder = "./Data_Organised/All_Strains_Comparison"
allFiles = os.listdir(folder)
multiSizerFiles = [allFiles[i] for i in range(len(allFiles)) if allFiles[i].endswith(".XLS")]
data = []
for files in multiSizerFiles:
    data.append(MultiSizerReader(path=os.path.join(folder,files)))

#split files into YD133 and YD133 + PWR20
cellType = []
labels = []
for d in data:
    if d.name.split("_")[0] == "BW25113":
        labels.append("Bw25113  \n OD: 0.1 ")
        cellType.append(1)
    if d.name.split("_")[0] == "MG1655":
        labels.append("MG1655 \n OD: 0.081 ")
        cellType.append(0)
    if d.name.split("_")[0] == "YD133+PWR20":
        labels.append("YD133 + PWR20 \n OD: 0.134 ")
        cellType.append(3)
    if d.name.split("_")[0] == "YD133":
        labels.append("YD133 \n OD: 0.190")
        cellType.append(2)


MultiSizerReader.plotData(data,groupValues=cellType,logAxis=False,labels=labels,legend=False,title="All strain comparison",xLims=(0.3,5))

combinedData,combinedTypes,combinedLabels = MultiSizerReader.sumByGroup(data,cellType,labels)
MultiSizerReader.plotData(combinedData,combinedTypes,labels=combinedLabels,logAxis=False,legend=True,
        title="All strain comparison (averaged)",logNormalFits=False,xLims=(0.3,5))

MultiSizerReader.boxPlotData(combinedData,groupValues=combinedTypes,labels=combinedLabels,title="All strain comparison")
