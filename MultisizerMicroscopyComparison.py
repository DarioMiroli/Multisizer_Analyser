from MultisizerReader import MultiSizerReader
import os
import matplotlib.pyplot as plt
import numpy as np

#Get all spread sheet files in fodler and create multisizer files for each
folder = "./Data_Organised/MultisizerMicroscopyComparison"
allFiles = os.listdir(folder)
multiSizerFiles = [allFiles[i] for i in range(len(allFiles)) if allFiles[i].endswith(".XLS")]
data = []
for files in multiSizerFiles:
    data.append(MultiSizerReader(path=os.path.join(folder,files)))

#Read csv file to get microscopy data
microVolumes = []
f = open("./Data_Organised/MultisizerMicroscopyComparison/M63_Glu_CAA_Volumes.csv")
for line in f.readlines():
    microVolumes.append(float(line.rstrip()))




#Subfigure plor
fig, ax = plt.subplots(nrows=1,ncols=2,figsize=(14,8))
combinedData,combinedTypes = MultiSizerReader.sumByGroup(data)
MultiSizerReader.plotData(combinedData,combinedTypes,labels=["Multisizer "],logAxis=False,logNormalFits=True,xLims=(0.0,3.2),showStats=False,ax=ax[0],alpha=0.5,density=True,text=False)

#Plot microscopy histogram
values,bins = np.histogram(microVolumes,bins=25,density=True)
x = np.asarray(bins)[:-1]
sep = 0.0
y=  values + sep
ax[0].step(x,y,where="pre",color="k",zorder=100)
ax[0].fill_between(x,y,sep,step="pre",zorder=100,alpha=0.5,label="Microscopy N:{0}".format(len(microVolumes)))
xPredict,yPredict, p0, p1 = MultiSizerReader.fitLogNormal(x,y)
ax[0].plot(xPredict,yPredict,linewidth=3,color="C3",label= "$\mu: {0:.3f}$ , $\sigma: {1:.3f}$".format(p0,p1),zorder=1000)
ax[0].legend(fontsize="xx-large")
ax[0].set_ylim(0,2.2)
#ax[0].errorbar([0.782,1.192,combinedData[0].getMean()],[2.1,2.2,2.3],xerr=[0.298,0.167,combinedData[0].getStDev()],fmt="None",ecolor="k",capsize=10,zorder=1000)


#Box plot on right hand plot
microData = MultiSizerReader()
microData.bins = x
microData.number =y

ax[1].bar(["Microscopy","Multisizer"],[0.789,1.192],yerr=[0.295,0.167],ecolor="k",capsize=10)
#ax[1].bar(["Microscopy","Multisizer"],[np.mean(microVolumes),combinedData[0].getMean()],yerr=[np.std(microVolumes),combinedData[0].getStDev()],ecolor="k",capsize=10)
ax[1].tick_params(axis="y", labelsize=20)
ax[1].tick_params(axis="x", labelsize=20)
ax[1].set_ylim(0,2.2)
ax[1].set_ylabel("Mean cell volume ($\mathbf{\mu m^3}$)",fontsize=20,weight="bold")
ax[0].text(0.05, 0.9 , "A", transform=ax[0].transAxes, size=35, weight='bold')
ax[1].text(0.05, 0.9 , "B", transform=ax[1].transAxes, size=35, weight='bold')
fig.tight_layout()
plt.show()
