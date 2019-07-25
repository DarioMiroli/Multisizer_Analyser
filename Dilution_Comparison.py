from MultisizerReader import MultiSizerReader
import os
import matplotlib.pyplot as plt

#Get all spread sheet files in fodler and create multisizer files for each
folder = "./Data_Organised/Dilution_Comparisons"
allFiles = os.listdir(folder)
multiSizerFiles = [allFiles[i] for i in range(len(allFiles)) if allFiles[i].endswith(".XLS")]
data = []
for files in multiSizerFiles:
    data.append(MultiSizerReader(path=os.path.join(folder,files)))

#split files into YD133 and YD133 + PWR20
ODs = []
labels = []
dilutions =[]
for d in data:
    OD = d.name.split("_")[4] + "." + d.name.split("_")[5]
    if d.name.split("_")[2] == "5":
        dilutions.append("$10^5$")
        labels.append("OD: {}".format(OD))
    if d.name.split("_")[2] == "7":
        dilutions.append("$10^7$")
        labels.append("OD: {}".format(OD))
    ODs.append(float(OD))

fig, ax = plt.subplots(nrows=2,ncols=2,figsize=(14,12))

MultiSizerReader.plotData(data,groupValues=ODs,joymode=False,logAxis=False,labels=labels,
        legend=False,title="",xLims=(0.4,4),colorScale=True,text=False,showStats=False,ax=ax[0][0],cbarLabel="$\mathbf{OD_{600}}$")

combinedData,combinedTypes,combinedLabels = MultiSizerReader.sumByGroup(data,ODs,labels)
MultiSizerReader.plotData(combinedData,combinedTypes,labels=combinedLabels,logAxis=False,legend=False,title="",logNormalFits=True,xLims=(0.4,4),colorScale=True,smoothing=5,showStats=False,ax=ax[0][1],text=False,cbarLabel="$\mathbf{OD_{600}}$")

MultiSizerReader.boxPlotData(combinedData,groupValues=combinedTypes,labels=None,title="", xlabel = "$\mathbf{OD_{600}}$", ylabel="Volume $\mathbf{\mu m ^3}$" ,ax=ax[1][0],positions=combinedTypes,logAxis=True,violin=False)
ax[1][0].set_ylim(0,4.5)


#****************** Bottom right plot ******
means = [d.getMean() for d in combinedData]
stds = [d.getStDev() for d in combinedData]
#ax[1][1].errorbar(combinedTypes,means,yerr=stds,ecolor="k",elinewidth=3,capsize=10,fmt="o--")
means = [d.getMode() for d in combinedData]
#ax[1][1].errorbar(combinedTypes,means,yerr=stds,ecolor="k",elinewidth=3,capsize=10,fmt="o--")

mus = [1.46,1.43,1.39,1.42,1.41,1.40,1.40,1.38,1.19,1.20,1.17,1.20,1.17,1.24,1.18,1.11,0.83]
sigmas = [0.23,0.22,0.20,0.22,0.20,0.21,0.20,0.20,0.17,0.20,0.18,0.19,0.21,0.19,0.18,0.18,0.19]
ax[1][1].errorbar(combinedTypes,mus,yerr=sigmas,ecolor="k",elinewidth=3,capsize=10,fmt="o--")
ax[1][1].set_xscale("log")
ax[1][1].set_xlabel("$\mathbf{OD_{600}}$",fontsize=20,fontweight="bold")
ax[1][1].set_ylabel("Mean cell volume ($\mathbf{\mu m ^3}$)",fontsize=20,fontweight="bold")
ax[1][1].tick_params(axis="x", labelsize=15)
ax[1][1].tick_params(axis="y", labelsize=15)
ax[0][0].text(0.90, 0.87 , "A", transform=ax[0][0].transAxes, size=35, weight='bold',color="gray")
ax[0][1].text(0.90, 0.87 , "B", transform=ax[0][1].transAxes, size=35, weight='bold',color="gray")
ax[1][0].text(0.90, 0.87 , "C", transform=ax[1][0].transAxes, size=35, weight='bold',color="gray")
ax[1][1].text(0.90, 0.87 , "D", transform=ax[1][1].transAxes, size=35, weight='bold',color="gray")


fig.tight_layout()
plt.savefig("./Graphs/ThesisFigures/GrowthCurve.png")
plt.savefig("./Graphs/ThesisFigures/GrowthCurve.pdf")

plt.show()
