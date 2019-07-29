import os
from MultisizerReader import MultiSizerReader
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rc,rcParams

fig, ax = plt.subplots(nrows=1,ncols=2,figsize=(14,8))


#Get all spread sheet files in fodler and create multisizer files for each
folders = [ "./Data_Organised/LB_YD133_PWR20_600mM_NaCl"]

ODs =[]
data =[]
for i,folder in enumerate(folders):
    allFiles = os.listdir(folder)
    multiSizerFiles = [allFiles[i] for i in range(len(allFiles)) if allFiles[i].endswith(".XLS")]
    for file in multiSizerFiles:
        data.append(MultiSizerReader(path=os.path.join(folders[i],file)))


ODs = [float(data[i].name.split("_")[4] + "." + data[i].name.split("_")[5]) for i in range(len(data))]

MultiSizerReader.plotData(data,groupValues=list(np.asarray(ODs)*1),labels=ODs,ax=ax[1],title="LB + 600mM NaCl",logAxis=False,legend=False,colorScale=True,text=False,showStats=False)



#Get all spread sheet files in fodler and create multisizer files for each
folders = [ "./Data_Organised/LB_YD133_PWR20"]

ODs =[]
data =[]
for i,folder in enumerate(folders):
    allFiles = os.listdir(folder)
    multiSizerFiles = [allFiles[i] for i in range(len(allFiles)) if allFiles[i].endswith(".XLS")]
    for file in multiSizerFiles:
        data.append(MultiSizerReader(path=os.path.join(folders[i],file)))


ODs = [float(data[i].name.split("_")[3] + "." + data[i].name.split("_")[4]) for i in range(len(data))]
MultiSizerReader.plotData(data,groupValues=list(np.asarray(ODs)*1),labels=ODs,ax=ax[0],title="LB",logAxis=False,legend=False,colorScale=True,text=False,showStats=False)
ax[0].text(0.05, 1.01 , "A", transform=ax[0].transAxes, size=35, weight='bold')
ax[1].text(0.05, 1.01 , "B", transform=ax[1].transAxes, size=35, weight='bold')
fig.tight_layout()
plt.show()
