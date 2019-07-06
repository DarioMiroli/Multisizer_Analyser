from MultisizerReader import MultiSizerReader
import os


#Get all spread sheet files in fodler and create multisizer files for each
folder = "./Data_Organised/YD133_Plasmid_Comparison_Expo"
allFiles = os.listdir(folder)
multiSizerFiles = [allFiles[i] for i in range(len(allFiles)) if allFiles[i].endswith(".XLS")]
data = []
for files in multiSizerFiles:
    data.append(MultiSizerReader(path=os.path.join(folder,files)))

#split files into YD133 and YD133 + PWR20
cellType = []
labels = []
for d in data:
    if d.name.split("_")[0] == "WT":
        labels.append("YD133 OD: 0.12 ")
        cellType.append(0)
    if d.name.split("_")[0] == "PW":
        labels.append("YD133 + PWR20 OD: 0.98 ")
        cellType.append(1)


MultiSizerReader.plotData(data,groupValues=cellType,labels=labels,legend=True,title="YD133  vs YD133 + PWR20 comparison")

combinedData,combinedTypes,combinedLabels = MultiSizerReader.sumByGroup(data,cellType,labels)
MultiSizerReader.plotData(combinedData,combinedTypes,labels=combinedLabels,legend=True,title="YD133 vs YD133 + PWR20 comparison")
