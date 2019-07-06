from MultisizerReader import MultiSizerReader
import os


#Get all spread sheet files in fodler and create multisizer files for each
folder = "./Data_Organised/YD133_600mMNaCl_Comparison"
allFiles = os.listdir(folder)
multiSizerFiles = [allFiles[i] for i in range(len(allFiles)) if allFiles[i].endswith(".XLS")]
data = []
for files in multiSizerFiles:
    data.append(MultiSizerReader(path=os.path.join(folder,files)))

#split files into YD133 and YD133 + PWR20
cellType = []
labels = []
for d in data:
    if d.name.split("_")[1] == "M63600":
        labels.append("600mM NaCl \n OD:0.086 ")
        cellType.append(0)
    if d.name.split("_")[1] == "OD":
        labels.append("0mM NaCl \n OD: 0.98")
        cellType.append(1)


MultiSizerReader.plotData(data,groupValues=cellType,labels=labels,legend=False,title="YD133 600mM NaCl comparsion")

combinedData,combinedTypes,combinedLabels = MultiSizerReader.sumByGroup(data,cellType,labels)
MultiSizerReader.plotData(combinedData,combinedTypes,labels=combinedLabels,legend=True,title="YD133 600mM NaCl comparsion averaged")
MultiSizerReader.boxPlotData(combinedData,groupValues=combinedTypes,labels=combinedLabels,title="YD133 600mM NaCl comparsion averaged")
