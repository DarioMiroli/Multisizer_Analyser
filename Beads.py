from MultisizerReader import MultiSizerReader
import os
import matplotlib.pyplot as plt
import numpy as np
#Get all spread sheet files in fodler and create multisizer files for each
folder = "./Data_Organised/Beads"
allFiles = os.listdir(folder)
multiSizerFiles = [allFiles[i] for i in range(len(allFiles)) if allFiles[i].endswith(".XLS")]
data = []
for files in multiSizerFiles:
    data.append(MultiSizerReader(path=os.path.join(folder,files)))


#Subfigure plot
fig, ax = plt.subplots(nrows=1,ncols=2,figsize=(14,8))


MultiSizerReader.plotData(data,logAxis=False,legend=True,title="Beads",xLims=(1,2.2),showStats=False,ax=ax[0],diameter=True,joymode=False,density=False)
combinedData,combinedTypes = MultiSizerReader.sumByGroup(data)
MultiSizerReader.plotData(combinedData,combinedTypes,logAxis=False,title="Beads (averaged)",logNormalFits=True,xLims=(1.2,2.2),showStats=False,ax=ax[1],diameter=True)
#MultiSizerReader.boxPlotData(combinedData,title="Beads",ax=ax[1][0])
ax[1].axvline(1.5,linewidth=3,label="Manufacturers diameter", color = "C2")
#ax[1].axvline(      ((3*combinedData[0].getMean()/(4*np.pi))**(1/3))*2     , linewidth=3, label="Distribution mean", color = "C3")
ax[1].legend(fontsize="x-large")
ax[0].text(0.05, 0.9 , "A", transform=ax[0].transAxes, size=35, weight='bold')
ax[1].text(0.05, 0.9 , "B", transform=ax[1].transAxes, size=35, weight='bold')
ax[1].set_ylim(0)
fig.tight_layout()
plt.show()
