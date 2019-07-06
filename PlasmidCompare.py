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



#Sum data with same OD (move to function soon)

combinedTypes = [0,1]
combinedLabels = ["YD133 + PWR20 OD:0.98 ","YD133 OD: 0.12 "]
combinedData = [MultiSizerReader() for i in range((2))]
for i in range(2):
    indices = [k for k,type in enumerate(cellType) if type==i]
    combinedData[i].bins = data[indices[0]].bins
    newNumbersList = data[indices[0]].number
    for index in indices:
        for j,n in enumerate(newNumbersList):
            newNumbersList[j] = n + data[index].number[j]
    combinedData[i].number = newNumbersList
    combinedData[i].totalCount = sum(newNumbersList)
combinedData.reverse()
MultiSizerReader.plotData(combinedData,groupValues=[0,1],labels=combinedLabels,legend=True,title="YD133 vs YD133 + PWR20 comparison")
