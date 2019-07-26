import os
from MultisizerReader import MultiSizerReader
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rc,rcParams
#Get all spread sheet files in fodler and create multisizer files for each
folders = [ "./Data_Organised/YD133+PWR20_000_GrowthCurve","./Data_Organised/YD133+PWR20_200_GrowthCurve",
             "./Data_Organised/YD133+PWR20_400_GrowthCurve","./Data_Organised/YD133+PWR20_600_GrowthCurve/All"]
concentrations = ["0","200","400","600"]
dataDic = {}
for i,folder in enumerate(folders):
    allFiles = os.listdir(folder)
    multiSizerFiles = [allFiles[i] for i in range(len(allFiles)) if allFiles[i].endswith(".XLS")]
    data = []
    for files in multiSizerFiles:
        data.append(MultiSizerReader(path=os.path.join(folder,files)))
    dataDic[concentrations[i]] = data


combinedDataDic = {}
titles = ["0mM NaCl","200mM NaCl","400mM NaCl","600mM NaCl"]
for i,key in enumerate(concentrations):

    data = dataDic[key]
    ODList = [float(data[i].name.split("_")[3] + "." + data[i].name.split("_")[4]) for i in range(len(data)) ]
    #Inspect all individual traces
    #MultiSizerReader.plotData(dataDic[key],ODList,ODList,legend=False,logAxis=False,xLims=(0.4,5),title=key,joymode= False)
    combinedData,combinedODs = MultiSizerReader.sumByGroup(data,ODList)
    for j,d in enumerate(combinedData): d.OD = combinedODs[j]

    combinedDataDic[key] = combinedData
    labels = ["OD: {} ".format(k) for k in combinedODs]
    if False:
        #Inspect collected traces
        rc('axes', linewidth=2)
        rc('font', weight='bold')
        fig, ax = plt.subplots(nrows=1,ncols=2,figsize=(14,9))
        MultiSizerReader.plotData(combinedData,combinedODs,labels,legend=False,text=False,logNormalFits=True,smoothing=5,logAxis=False,xLims=(0.4,5),title=titles[i],joymode= False,ax=ax[0],colorScale=True,cbarLabel="$\mathbf{OD_{600}}$")
        medians = [c.getMedian() for c in combinedData]
        MADs = [c.getMAD() for c in combinedData]
        ax[1].errorbar(combinedODs,medians,yerr=MADs , fmt='o--',ecolor="k",capsize=5)
        ax[1].set_xscale("log")
        ax[1].set_xticks([0.001,0.01,0.1,1])
        ax[1].set_ylim(0,3)
        ax[1].set_xlim(0.0009,6)
        ax[1].xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
        ax[0].text(0.90, 0.93 , "A", transform=ax[0].transAxes, size=35, weight='bold',color="k")
        ax[1].text(0.90, 0.93 , "B", transform=ax[1].transAxes, size=35, weight='bold',color="k")
        ax[1].set_xlabel("$\mathbf{OD_{600}}$",fontsize=20,weight="bold")
        ax[1].set_ylabel("Median volume ($\mathbf{\mu m^3}$)",fontsize=20,weight="bold")

        ax[1].tick_params(axis="x", labelsize=19)
        ax[1].tick_params(axis="y", labelsize=19)
        fig.tight_layout()
        plt.show()

#Plot averages (stats summary)
rc('axes', linewidth=2)
rc('font', weight='bold')
fig, ax = plt.subplots(nrows=1,ncols=2,figsize=(14,11))
rc('font', weight='bold')
ax1 = plt.subplot2grid((2,2), (0, 0), colspan=2)
rc('font', weight='bold')
ax2 = plt.subplot2grid((2,2), (1, 0))
rc('font', weight='bold')
ax3 = plt.subplot2grid((2,2), (1, 1))
rc('font', weight='bold')

ax = [ax1,ax2,ax3]

lowODs = [0.059,0.063,0.059,0.048]
highODs = [0.132,0.112,0.136,0.171]
c = 0
for key in concentrations:
    condition = key
    dataList  =  combinedDataDic[key]
    ODs = [d.OD for d in dataList ]
    means = np.asarray([d.getMean() for d in dataList])
    modes = np.asarray([d.getMode() for d in dataList])
    medians = np.asarray([d.getMedian() for d in dataList])
    MADs = [d.getMAD() for d in dataList]
    stdevs = np.asarray([d.getStDev() for d in dataList])
    p = ax[0].plot(ODs,medians,'o--',label=key+" mM NaCl")
    ax[0].plot(lowODs[c],medians[ODs.index(lowODs[c])],'^',markersize=12,color="C{}".format(c))
    ax[0].plot(highODs[c],medians[ODs.index(highODs[c])],'s',markersize=12,color="C{}".format(c))

    ax[0].fill_between(ODs,medians+MADs,medians-MADs,alpha=0.1)
    #plt.plot(ODs,modes,"*",c=p[0].get_color())
    c = c + 1
ax[0].set_xscale("log")
ax[0].set_ylim(0.6,2)

for item in ([ax[0].title,ax[0].xaxis.label, ax[0].yaxis.label] + ax[0].get_xticklabels() + ax[0].get_yticklabels()):
    item.set_fontsize(20)
ax[0].set_xticks([0.001,0.003,0.01,0.03,0.1,0.3,1,4])
ax[0].xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax[0].legend(fontsize="x-large")
ax[0].tick_params(axis="x", labelsize=15)
ax[0].set_xlabel("OD$\mathbf{_{600}}$",weight="bold")
ax[0].set_ylabel("Median cell volume $\mathbf{\mu m^3}$",weight="bold")
ax[0].set_title("Cell size at high osmollarity",fontsize=20,weight="bold")
ax[0].xaxis.grid(True)



ODs = [0.059,0.063,0.059,0.048]
comparisonData = []
labels = []
concs = []
means = []
for i in range(len(ODs)):
    print(type(combinedDataDic[concentrations[i]]))
    for d in combinedDataDic[concentrations[i]]:
        if d.OD == ODs[i]:
            comparisonData.append(d)
            labels.append("{} mM NaCl ".format(concentrations[i]))
            concs.append(concentrations[i])
            means.append(d.getMean())
rc('font', weight='bold')
MultiSizerReader.plotData(comparisonData,colors=["C0","C1","C2","C3","C4"],alpha=0.75,logNormalFits=False,labels=labels,ax=ax[1],smoothing=3,text=False,legend=True,logAxis=False,xLims=(0.4,5),title="Cell size at OD$\mathbf{_{600}}$ ~0.06",joymode= False)


ODs = [0.132,0.112,0.136,0.171]
comparisonData = []
labels = []
concs = []
means = []
for i in range(len(ODs)):
    print(type(combinedDataDic[concentrations[i]]))
    for d in combinedDataDic[concentrations[i]]:
        if d.OD == ODs[i]:
            comparisonData.append(d)
            labels.append("{} mM NaCl ".format(concentrations[i]))
            concs.append(concentrations[i])
            means.append(d.getMean())
rc('font', weight='bold')
MultiSizerReader.plotData(comparisonData,colors=["C0","C1","C2","C3","C4"],alpha=0.75,logNormalFits=False,labels=labels,ax=ax[2],smoothing=3,text=False,legend=True,logAxis=False,xLims=(0.4,5),title="Cell size at OD$\mathbf{_{600}}$ ~0.15",joymode= False)

#MultiSizerReader.boxPlotData(comparisonData,labels=concentrations,ax=ax[2],title="Osmo comparison OD ~0.06",positions=[0.0,2.0,4.0,6.0])
fig.tight_layout()
ax[0].text(0.01, 0.85 , "A", transform=ax[0].transAxes, size=30, weight='bold')
ax[1].text(0.02, 0.85 , "B", transform=ax[1].transAxes, size=30, weight='bold')
ax[2].text(0.02, 0.85 , "C", transform=ax[2].transAxes, size=30, weight='bold')
ax[1].legend(prop={'size':14,"weight":"bold"})
ax[2].legend(prop={'size':14,"weight":"bold"})
plt.savefig("Graphs/ThesisFigures/OsmoGrowthCurves.png")
plt.savefig("Graphs/ThesisFigures/OsmoGrowthCurves.pdf")



plt.show()
exit()


plt.plot(concs,means,"--o")
plt.xlabel("NaCl Concentration (mM)")
plt.ylabel("Mean cell volume $\mu m^3$")
plt.tight_layout()
plt.show()

exit()






#Median low OD plot ************************************************************
comparisonData = []
labels = []
concs = []
means = []
for i in range(len(ODs)):
    print(type(combinedDataDic[concentrations[i]]))
    for d in combinedDataDic[concentrations[i]]:
        if d.OD == ODs[i]:
            comparisonData.append(d)
            labels.append("{} mM NaCl ".format(concentrations[i]))
            concs.append(concentrations[i])
            means.append(d.getMean())
rc('font', weight='bold')
MultiSizerReader.plotData(comparisonData,colors=["C0","C1","C2","C3","C4"],alpha=0.75,logNormalFits=False,labels=labels,ax=ax[2],smoothing=3,text=False,legend=True,logAxis=False,xLims=(0.4,5),title="Cell size at OD$\mathbf{_{600}}$ ~0.15",joymode= False)
