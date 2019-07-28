import os
from MultisizerReader import MultiSizerReader
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rc,rcParams
#Get all spread sheet files in fodler and create multisizer files for each
#folders = [ "./Data_Organised/YD133+PWR20_000_GrowthCurve","./Data_Organised/YD133+PWR20_200_GrowthCurve",
#             "./Data_Organised/YD133+PWR20_400_GrowthCurve","./Data_Organised/YD133+PWR20_600_GrowthCurve/All"]
#concentrations = ["0","200","400","600"]
folders = [ "./Data_Organised/YD133+PWR20_000_GrowthCurve","./Data_Organised/YD133+PWR20_300_Sorbitol_GrowthCurve","./Data_Organised/YD133+PWR20_600_Sorbitol_GrowthCurve"]
concentrations = ["0","300","600"]


dataDic = {}
for i,folder in enumerate(folders):
    allFiles = os.listdir(folder)
    multiSizerFiles = [allFiles[i] for i in range(len(allFiles)) if allFiles[i].endswith(".XLS")]
    data = []
    for files in multiSizerFiles:
        data.append(MultiSizerReader(path=os.path.join(folder,files)))
    dataDic[concentrations[i]] = data


combinedDataDic = {}
titles = ["0mM Sorbitol","300mM Sorbitol","600mM Sorbitol"]
for i,key in enumerate(concentrations):

    data = dataDic[key]
    if i ==0 :
        ODList = [float(data[i].name.split("_")[3] + "." + data[i].name.split("_")[4]) for i in range(len(data)) ]
    else:
        ODList = [float(data[i].name.split("_")[5] + "." + data[i].name.split("_")[6]) for i in range(len(data)) ]

    #Inspect all individual traces
    #MultiSizerReader.plotData(dataDic[key],ODList,ODList,legend=False,logAxis=False,xLims=(0.4,5),title=key,joymode= False)
    combinedData,combinedODs = MultiSizerReader.sumByGroup(data,ODList)
    for j,d in enumerate(combinedData): d.OD = combinedODs[j]

    combinedDataDic[key] = combinedData
    labels = ["OD: {} ".format(k) for k in combinedODs]
    if True:
        #Inspect collected traces
        rc('axes', linewidth=2)
        rc('font', weight='bold')
        fig, ax = plt.subplots(nrows=1,ncols=2,figsize=(14,9))
        MultiSizerReader.plotData(combinedData,combinedODs,labels,legend=False,title="", text=False,logNormalFits=True,smoothing=5,logAxis=False,xLims=(0.4,5),joymode= False,ax=ax[0],colorScale=True,cbarLabel="$\mathbf{OD_{600}}$")
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
        fig.suptitle(titles[i], fontsize=25,weight="bold")
        ax[1].tick_params(axis="x", labelsize=19)
        ax[1].tick_params(axis="y", labelsize=19)
        fig.tight_layout()
        fig.subplots_adjust(top=0.90)
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

lowODs = [0.059,0.054,0.077]
highODs = [0.132,0.132,0.172]
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
    p = ax[0].plot(ODs,medians,'o--',label=key+" mM sorbitol")
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



ODs =lowODs
comparisonData = []
labels = []
concs = []
means = []
for i in range(len(ODs)):
    print(type(combinedDataDic[concentrations[i]]))
    for d in combinedDataDic[concentrations[i]]:
        if d.OD == ODs[i]:
            comparisonData.append(d)
            labels.append("{} mM sorbitol ".format(concentrations[i]))
            concs.append(concentrations[i])
            means.append(d.getMean())
rc('font', weight='bold')
MultiSizerReader.plotData(comparisonData,colors=["C0","C1","C2","C3","C4"],alpha=0.75,logNormalFits=False,labels=labels,ax=ax[1],smoothing=3,text=False,legend=True,logAxis=False,xLims=(0.4,5),title="Cell size at OD$\mathbf{_{600}}$ ~0.06",joymode= False)


ODs = highODs
comparisonData = []
labels = []
concs = []
means = []
for i in range(len(ODs)):
    print(type(combinedDataDic[concentrations[i]]))
    for d in combinedDataDic[concentrations[i]]:
        if d.OD == ODs[i]:
            comparisonData.append(d)
            labels.append("{} mM Sorbitol ".format(concentrations[i]))
            concs.append(concentrations[i])
            means.append(d.getMean())
rc('font', weight='bold')
MultiSizerReader.plotData(comparisonData,colors=["C0","C1","C2","C3","C4"],alpha=0.75,logNormalFits=False,labels=labels,ax=ax[2],smoothing=3,text=False,legend=True,logAxis=False,xLims=(0.4,5),title="Cell size at OD$\mathbf{_{600}}$ ~0.15",joymode= False)

#MultiSizerReader.boxPlotData(comparisonData,labels=concentrations,ax=ax[2],title="Osmo comparison OD ~0.06",positions=[0.0,2.0,4.0,6.0])
fig.tight_layout()
ax[0].text(0.01, 0.85 , "A", transform=ax[0].transAxes, size=30, weight='bold')
ax[1].text(0.02, 0.85 , "B", transform=ax[1].transAxes, size=30, weight='bold')
ax[2].text(0.01, 0.85 , "C", transform=ax[2].transAxes, size=30, weight='bold')
ax[1].legend(prop={'size':14,"weight":"bold"})
ax[2].legend(prop={'size':14,"weight":"bold"})
plt.savefig("Graphs/ThesisFigures/OsmoGrowthCurves.png")
plt.savefig("Graphs/ThesisFigures/OsmoGrowthCurves.pdf")



plt.show()


































#Median low OD plot ************************************************************
medians = []
means = []
MADs = []
stds = []
for i in range(len(concentrations)):
    tempMedians = []
    tempMADs = []
    tempMeans = []
    for d in combinedDataDic[concentrations[i]]:
        if d.OD > 0.1 and d.OD < 0.3:
            tempMedians.append(d.getMedian())
            tempMADs.append(d.getMAD())
            tempMeans.append(d.getMean())
    medians.append(np.mean(tempMedians))
    MADs.append(np.max(tempMADs))
    stds.append(np.std(tempMedians))
    means.append(np.mean(tempMeans))
stds[1] = stds[2]
rc('axes', linewidth=2)
rc('font', weight='bold')
fig, ax = plt.subplots(nrows=2,ncols=2,figsize=(14,9))
concentrations = [float(i) for i in concentrations]
#concentrations = [328, 666.6666667, 1212 ]
concentrations= [0,300,600]
ax = [ax[0][0],ax[0][1],ax[1][0],ax[1][1]]
ax[0].errorbar(concentrations,medians,yerr=MADs,fmt='--',ecolor="k",linewidth=3,capsize=10,color="C4")
ax[0].scatter(concentrations,medians,c=["C0","C1","C2"],zorder=999,s=50,marker="d")
#microConcentrations = [0,200,400,600]
microConcentrations = [0,300]
#microConcentrations = [328,666.6666667]
#microscopyMeans = np.asarray([0.8737279444271844, 0.9431799287878111, 0.8079749981938046, 0.8834669500128371, 0.8467358421385968])
#microscopyMedians = np.asarray([0.83359016783446, 0.9107193566167346,  0.768655633624957, 0.8505402300531674, 0.8241851581944356])
#microscopyMADs = np.asarray([0.20530786139031398, 0.23552065787144438,  0.18137993944495723,  0.21282503163497035, 0.2203573124500564])
#microscopyErr = np.asarray([0.019592024593452443, 0.019858896585265597,0.014585367867718432,  0.013730517611745794, 0.01983280598275184])
microscopyMeans = np.asarray([0.8737279444271844, 0.8079749981938046])
microscopyMedians = np.asarray([0.83359016783446,  0.768655633624957])
microscopyMADs = np.asarray([0.20530786139031398,  0.18137993944495723])
microscopyErr = np.asarray([0.019592024593452443,0.014585367867718432])

ax[0].errorbar(microConcentrations,microscopyMedians,yerr=microscopyMADs,fmt='--',ecolor="gray",linewidth=3,capsize=10,color="C5")
ax[0].scatter(microConcentrations,microscopyMedians,c=["C{0}".format(i) for i in range(len(microConcentrations))],zorder=999,s=50,marker="s")

#Mean stuff
ax[2].errorbar(concentrations,means,yerr=stds,fmt='--',ecolor="k",linewidth=3,capsize=10,color="C4")
ax[2].scatter(concentrations,means,c=["C0","C1","C2"],zorder=999,s=50,marker="d")
ax[2].errorbar(microConcentrations,microscopyMeans,yerr=microscopyErr,fmt='--',ecolor="gray",linewidth=3,capsize=10,color="C5")
ax[2].scatter(microConcentrations,microscopyMeans,c=["C{0}".format(i) for i in range(len(microConcentrations))],zorder=999,s=50,marker="s")


microscopyErr = microscopyErr/(microscopyMeans[0])
print(MADs)
print(medians[0])
MADs = MADs/medians[0]
print(MADs)
microscopyMADs = microscopyMADs/microscopyMedians[0]
stds = stds/(medians[0])


medians = medians/(medians[0])
microscopyMeans = microscopyMeans/microscopyMeans[0]
microscopyMedians = microscopyMedians/microscopyMedians[0]
means = means/means[0]



ax[1].errorbar(concentrations,medians,yerr=MADs,fmt='--',ecolor="k",linewidth=3,capsize=10,color="C4")
ax[1].scatter(concentrations,medians,c=["C0","C1","C2"],zorder=999,s=50,marker="d")
ax[1].errorbar(microConcentrations, microscopyMedians,yerr=microscopyMADs,fmt='--',ecolor="gray",linewidth=3,capsize=10,color="C5")
ax[1].scatter(microConcentrations, microscopyMedians,c=["C{0}".format(i) for i in range(len(microConcentrations))],zorder=999,s=50,marker="s")

#Mean stuff
ax[3].errorbar(concentrations,means,yerr=stds,fmt='--',ecolor="k",linewidth=3,capsize=10,color="C4")
ax[3].scatter(concentrations,means,c=["C0","C1","C2"],zorder=999,s=50,marker="d")
ax[3].errorbar(microConcentrations,microscopyMeans,yerr=microscopyErr,fmt='--',ecolor="gray",linewidth=3,capsize=10,color="C5")
ax[3].scatter(microConcentrations,microscopyMeans,c=["C{0}".format(i) for i in range(len(microConcentrations))],zorder=999,s=50,marker="s")


ax[0].set_ylim(0.4,1.8)
ax[1].set_ylim(0.4,1.4)
ax[0].set_xlabel("Sorbitol Concentration (mM)",fontweight="bold",fontsize=15)
ax[1].set_xlabel("Sorbitol Concentration (mM)",fontweight="bold",fontsize=15)
ax[0].set_ylabel("Median volume ($\mathbf{\mu m^3}$) ",fontweight="bold",fontsize=15)
ax[1].set_ylabel("Normalised median volume",fontweight="bold",fontsize=15)
ax[0].tick_params(axis="x", labelsize=15)
ax[0].tick_params(axis="y", labelsize=15)
ax[1].tick_params(axis="x", labelsize=15)
ax[1].tick_params(axis="y", labelsize=15)

ax[2].set_ylim(0.4,1.8)
ax[3].set_ylim(0.4,1.4)
ax[2].set_xlabel("Sorbitol Concentration (mM)",fontweight="bold",fontsize=15)
ax[3].set_xlabel("Sorbitol Concentration (mM)",fontweight="bold",fontsize=15)
ax[2].set_ylabel("Mean volume ($\mathbf{\mu m^3}$)",fontweight="bold",fontsize=15)
ax[3].set_ylabel("Normalised mean volume",fontweight="bold",fontsize=15)
#ax[1].axhline(1.0,color="gray")
#ax[3].axhline(1.0,color="gray")

ax[2].tick_params(axis="x", labelsize=15)
ax[2].tick_params(axis="y", labelsize=15)
ax[3].tick_params(axis="x", labelsize=15)
ax[3].tick_params(axis="y", labelsize=15)
ax[0].text(0.05, 0.85 , "A", transform=ax[0].transAxes, size=35, weight='bold')
ax[1].text(0.05, 0.85 , "B", transform=ax[1].transAxes, size=35, weight='bold')
ax[2].text(0.05, 0.85 , "C", transform=ax[2].transAxes, size=35, weight='bold')
ax[3].text(0.05, 0.85 , "D", transform=ax[3].transAxes, size=35, weight='bold')

from matplotlib.lines import Line2D
lines = [ Line2D([0], [0], marker=shape, color='w',markerfacecolor='k', markersize=10) for shape in ["d","s"] ]
labels = ["Multisizer Data", "Microscopy Data"]
ax[0].legend(lines, labels, fontsize="x-large",loc="lower center",ncol=2)
ax[1].legend(lines, labels, fontsize="x-large",loc="lower center",ncol=2)
ax[2].legend(lines, labels, fontsize="x-large",loc="lower center",ncol=2)
ax[3].legend(lines, labels, fontsize="x-large",loc="lower center",ncol=2)
ax[1].yaxis.grid(True)
ax[3].yaxis.grid(True)


fig.tight_layout()
plt.show()
