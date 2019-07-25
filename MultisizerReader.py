import os
import numpy as np
import matplotlib
matplotlib.rcParams["savefig.directory"] = os.chdir(os.path.dirname(__file__))
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats
import seaborn as sns
from matplotlib import rc,rcParams
rc('axes', linewidth=2)
rc('font', weight='bold')
rcParams['text.latex.preamble'] = [r'\boldmath']



class MultiSizerReader:

    def __init__(self,path=None):
        self.path = path
        if self.path == None:
            self.name = None
            self.bins = None
            self.number = None
            self.numberPercent = None
            self.totalCount = 0

        else:
            self.name = os.path.basename(self.path)
            self.loadMultiSizerSheet()
        #print("Multisizer Object. Name: {} N: {}".format(self.name,self.totalCount))

    def loadMultiSizerSheet(self):
        '''Loads multisizer spread sheet data into newley created
        MultiSizerReaderObject'''
        binsLowerEdge = []
        number = []
        numberPercent = []

        with open(self.path) as f:
            lines = f.readlines()
            startIndex = len(lines)
            for i,line in enumerate(lines):
                splitLine = line.split()
                if len(splitLine) > 0:
                    if splitLine[0] == "Bin":
                        #Add 3 here to skip extra lines of text before data
                        startIndex = i+3
                    if i >= startIndex and i < len(lines)-2:
                        if float(splitLine[0]) >= 0.4:
                            binsLowerEdge.append(float(splitLine[0]))
                            number.append(float(splitLine[1]))
                            numberPercent.append(float(splitLine[2]))
                    if i == len(lines)-2:
                        pass
                        #binsLowerEdge.append(float(splitLine[0]))
        self.bins = binsLowerEdge
        self.number = number
        self.numberPercent = numberPercent
        self.totalCount = np.sum(self.number)

    def plotData(dataList,groupValues = None, labels= None, alpha = 1.0, legend = True,
        spacing = 0.015,title= None,joymode = False,showStats=True,smoothing=1,logAxis=True,
        xLims=None,logNormalFits=False,ax=None,diameter=False, density=False, colorScale =False, text=True,cbarLabel="" ):
        '''
        Should plot joy like plots for all multisizer objects in list "dataList". Will color traces with same group value the same color
        '''
        if joymode == True:
            if ax != None:
                ax.patch.set_facecolor('black')
            if ax == None:
                plt.style.use("dark_background")
        else:
            plt.style.use("default")


        if ax == None:
            fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(12,8))
            show= True
        else:
            show = False


        #spacing = smoothing*spacing

        if groupValues == None:
            groupValues= [i for i in range(len(dataList))]
        if labels == None:
            labels = ["" for i in range(len(dataList))]
        noGroups = len(list(set(groupValues)))
        #Sort data by groups
        dataList = [dataItem for groupNo, dataItem in sorted(zip(groupValues,dataList), key=lambda pair: pair[0])]
        labels = [labelItem for groupNo, labelItem in sorted(zip(groupValues,labels), key=lambda pair: pair[0])]
        groupValues = sorted(groupValues)
        if colorScale == False:
            colors = plt.cm.jet(np.linspace(0,1,noGroups))
        else:
            colors =[]
            uniqueGroups = list(dict.fromkeys(groupValues))
            uniqueGroups = np.log10(uniqueGroups)
            for i in range(len(uniqueGroups)):
                normedValue = (uniqueGroups[i]-min(uniqueGroups))/(max(uniqueGroups)-min(uniqueGroups))
                colors.append(plt.cm.inferno(normedValue))
            from mpl_toolkits.axes_grid1 import make_axes_locatable
            divider = make_axes_locatable(ax)
            cax = divider.append_axes('right', size='5%', pad=0.05)
            fig = plt.gcf()
            cb = fig.colorbar( plt.cm.ScalarMappable(cmap=plt.cm.inferno, norm=matplotlib.colors.LogNorm(vmin=min(groupValues), vmax=max(groupValues))), cax=cax, orientation='vertical')
            #cb.ax.yaxis.set_ticks(np.logspace(np.log10(min(groupValues)), np.log10(max(groupValues)), 10))
            #cb.ax.yaxis.set_ticks([0.01,0.05,0.1,0.5,1.0,2.0,4.0])
            cb.ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
            cb.ax.tick_params(axis="y", labelsize=15)
            cb.ax.set_title(cbarLabel,fontweight="bold",fontsize=15)
        if xLims == None and logAxis == True:
            lowerXLim,upperXLim = (0.3,15)
        elif xLims == None and logAxis == False:
            lowerXLim,upperXLim = (0.3,10)
        else:
            lowerXLim,upperXLim = xLims


        c = noGroups-1
        zorder = [z for z in reversed(range(len(dataList)))]
        for i in reversed(range(len(dataList))):

            x = dataList[i].bins
            y = dataList[i].number
            if smoothing > 1:
                X,Y = MultiSizerReader.smoothData(x,y,smoothing)

            else:
                X,Y = x,y
            x = X
            #Convert volume to diameter
            if diameter:
                x = 2*np.power( 3*np.asarray(x)/(4*np.pi),1/3.0)
            binSpacings = np.asarray(  [x[i+1] - x[i] for i in range(len(x)-1)] )
            binSpacings = np.append(binSpacings,binSpacings[-1])
            if density == True:
                y = ((np.asarray(Y))/(sum(Y)*binSpacings)) + spacing*i
            else:
                y = ((np.asarray(Y))/(sum(Y))) + spacing*i
            y2 = [spacing*i for k in range(len(X))]

            if i != len(dataList)-1:
                if groupValues[i] != groupValues[i+1]:
                    c = c - 1

            #Draw fill between black line and new zero line and fit log normal
            if not joymode:
                ax.fill_between(x,y,y2, step="pre", alpha=alpha,color=colors[c], zorder = zorder[i], label=str(labels[i])+'N: {0}k'.format(int(dataList[i].totalCount/1000.0)))
            if logNormalFits == True:
                logNormalX,logNormalY, mu, sigma = MultiSizerReader.fitLogNormal(x,y-spacing*(i))

                ax.plot(logNormalX,logNormalY+spacing*i,"b",zorder=zorder[i],label = "$\mu$: {0:.2f} , $\sigma$ : {1:.2f}".format(mu,abs(sigma)),linewidth=3,color="C{0}".format(i))


            if showStats== True:
                totalNumber = sum(Y)
                cumulativeNumber = 0
                for n in range(len(Y)):
                    if cumulativeNumber > (totalNumber + 1)/2.0:
                        medianIndex = n
                        break
                    else:
                        cumulativeNumber = cumulativeNumber + Y[n]
                    median = X[n]
                average= sum([Y[k]*X[k] for k in range(len(Y))])/totalNumber
                ax.fill_between([x[medianIndex],x[medianIndex+1]],[y[medianIndex],y[medianIndex+1]],[y2[medianIndex],y2[medianIndex+1]], step="pre", alpha=alpha,color="k",zorder=zorder[i])

            if joymode == True:
                lineColor = "w"
            if joymode == False:
                lineColor = 'k'
            #Plot black line on top of hist
            ax.plot(x,y,color=lineColor,drawstyle="steps",zorder =zorder[i] )
            if legend == True:
                ax.legend(fontsize="x-large")
            if text == True:
                ax.text(lowerXLim + (upperXLim-lowerXLim)*0.6, y[-1]+0.001, str(labels[i]) + 'N: {0}k'.format(int(dataList[i].totalCount/1000.0)))

        for item in ([ax.title,ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(20)
        print(logAxis)
        if logAxis:
            ax.xscale("log")
            ax.set_xticks([0.2, 0.5,0.7, 1.0,2.0,4.0,6.0,8.0,10])
        ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
        if diameter:
            ax.set_xlabel("Equivalent spherical diameter $\mathbf{\mu m}$",fontsize=20,fontweight="bold")
        else:
            ax.set_xlabel("Volume $\mathbf{{\mu m^3}}$",fontsize=20,fontweight="bold")
        ax.set_ylabel("Relative Normalised Count",fontsize=20,fontweight="bold")
        if title != None:
            ax.set_title(title,fontsize=20,fontweight="bold")
        ax.set_xlim(lowerXLim,upperXLim)
        if show:
            fig.tight_layout()
            plt.show()

    def boxPlotData(dataList,groupValues = None, labels= None, title=None, xlabel= "X axis", ylabel= "Y axis", positions=None,ax=None,logAxis = False, violin = True, bWidth = 0.1, vWidth =0.1 ):
        '''
        Plot box plot of data coloring boxes by group color
        '''
        if ax == None:
            fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(12,8))
            show= True
        else:
            show = False

        if groupValues == None:
            groupValues= [i for i in range(len(dataList))]
        if labels == None:
            labels = ["" for i in range(len(dataList))]
        noGroups = len(list(set(groupValues)))
        #Sort data by groups
        dataList = [dataItem for groupNo, dataItem in sorted(zip(groupValues,dataList), key=lambda pair: pair[0])]
        labels = [labelItem for groupNo, labelItem in sorted(zip(groupValues,labels), key=lambda pair: pair[0])]
        groupValues = sorted(groupValues)
        colors = plt.cm.jet(np.linspace(0,1,noGroups))
        boxData = []
        for data in dataList:
            tempList = []
            for i in range(len(data.number)):
                tempList = tempList + [data.bins[i]]*int(data.number[i])
            boxData.append(tempList)

        #boxData = [boxData[i]/np.mean(boxData[0]) for i in range(len(boxData))]
        if logAxis:
            width = lambda p, w: 10**(np.log10(p)+w/2.)-10**(np.log10(p)-w/2.)


        else:
            width = lambda p, w: w
            ax.set_xscale("linear")
        bp = ax.boxplot(boxData,labels=labels,vert=True,sym='.',whis=[1,99],patch_artist=True,showmeans=True,positions=positions,widths=width(positions,bWidth))
        if violin:
            ax.violinplot(boxData, points=300, widths=width(positions,vWidth), vert=True, showmeans=False, showextrema=False, showmedians=False,positions=positions)
        #plt.plot([0,4,5,6],[4.6/4.6,3.8/4.6,3.9/4.6,3.5/4.6],'v--',zorder=999)
        if logAxis:
            ax.set_xscale("log")
        else:
            ax.set_xscale("linear")
        #sns.violinplot(data= boxData,orient="h",bw=0.08,cut=0,scale="area",gridsize=200, whis=[5, 100])
        #plt.gcf().get_axes()[0].set(yticklabels=labels)


        for box in bp['boxes']:
            # change outline color
            #box.set(color='red', linewidth=2)
            # change fill color
            box.set(facecolor = 'lightskyblue' )
            # change hatch
            #box.set(hatch = '/')
        plt.setp(bp["medians"], color="k")

        for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() ):
            item.set_fontsize(20)
        ax.set_xlabel(xlabel,fontsize=20,fontweight="bold")
        ax.set_ylabel(ylabel,fontsize=20,fontweight="bold")
        if title != None:
            ax.set_title(title,fontsize=20,fontweight="bold")
        ax.tick_params(axis="y", labelsize=15,)
        ax.tick_params(axis="x", labelsize=15)
        if show:
            fig.tight_layout()
            plt.show()

    def sumByGroup(dataList,groupValues=None,labels=None):
        '''
        Compiles multiple Multisizers files by summing their bins if they have the same groupValue. Size of lists "dataList" and "goupValues" should be the same
        '''
        if groupValues == None:
            groupValues = [0 for i in range(len(dataList))]
        #Sum data with same OD (move to function soon)
        combinedGroupValues = list(set(groupValues))
        combinedGroupValues.sort()
        combinedData = [MultiSizerReader() for i in range(len(combinedGroupValues))]
        for i,groupValue in enumerate(combinedGroupValues):
            indices = [k for k, x in enumerate(groupValues) if x == groupValue]
            combinedData[i].bins = dataList[indices[0]].bins
            newNumbersList = dataList[indices[0]].number
            for index in indices:
                for j,n in enumerate(newNumbersList):
                    newNumbersList[j] = n + dataList[index].number[j]
            combinedData[i].number = newNumbersList
            combinedData[i].totalCount = sum(newNumbersList)
            for n in range(len(combinedData[i].number)):
                combinedData[i].numberPercent = combinedData[i].number[n]/combinedData[i].totalCount
        if labels == None:
            return combinedData,combinedGroupValues
        else:
            combinedLabels = [ labels[groupValues.index(combinedGroupValues[i])]  for i in range(len(combinedGroupValues))]
            return combinedData,combinedGroupValues,combinedLabels

    def smoothData(bins,heights,binsToSmooth):
        '''
        Method which takes a list of bins and heights and smooths them by summing and grouping n bins where n = binsToSmooth
        '''
        bins = np.asarray(bins)
        heights = np.asarray(heights)
        newBins = []
        newHeights = []

        if binsToSmooth % 2 == 0:
            binsToSmooth = binsToSmooth + 1

        for i in range(len(bins)):
            stride = (binsToSmooth-1)/2
            lastBinIndex = stride + i
            if lastBinIndex <= len(bins)-1:
                newHeight = np.mean(heights[int(i-stride):int(i+stride+1)])
            if lastBinIndex > len(bins)-1:
                newHeight = np.mean(heights[int(i-stride):])
            if i < stride + 1 :
                newHeight = np.mean(heights[0:int(i+stride)])
            newHeights.append(newHeight)
            newBins.append(bins[i])
        return newBins, newHeights

        #index = 0
        #done = False
        #while not done:
        #    if index+binsToSmooth > len(bins) -1 :
        #        #Have some remainder left
        #        done = True
        #        newBins.append(bins[index])
        #        newHeights.append(sum(heights[index:index + (len(bins)-1-index)]))
        #    else:
        #        newBins.append(bins[index])
        #        newHeights.append(sum(heights[index:index+binsToSmooth]))
        #    index = index +  binsToSmooth
        #    #Perfectly fit into range
        #    if index == len(bins) -1:
        #        done = True
        #return newBins, newHeights

    def fitLogNormal(xs,ys):
        def logNormal(x,mu,sigma,k):
            prefactor = k/(x*sigma*(2*np.pi**0.5))
            exponent = ((np.log(x)-mu)**2)/(2*(sigma**2))
            yPredict = prefactor*np.exp(-1.0*exponent)
            return yPredict

        def gaussian(x,mu,sigma,k):
            prefactor = k/((2*np.pi*(sigma*sigma))**0.5)
            exponent = ((x-mu)**2)/(2*sigma*sigma)
            yPredict = prefactor*np.exp(-1.0*exponent)
            return yPredict
        #fit it
        popt, pcov = curve_fit(logNormal, xs, ys)
        #mu = 1.0
        #sigma = 0.2
        #k = 0.05
        #c =0
        #popt = [mu,sigma,k,c]
        xPredicted = np.linspace(start=min(xs),stop=max(xs),num=100000)
        yPredicted = logNormal(xPredicted,popt[0],popt[1],popt[2])
        return xPredicted,yPredicted, popt[0],popt[1]

    def getMean(self):
        ''' computes the average size of cells in file and returns it'''
        total = 0
        for i,bn in enumerate(self.bins):
            total = total + (bn*self.number[i])
        mean = total/sum(self.number)
        return mean

    def getMode(self):
        ''' computes the mode of cell size in the file and returns it'''
        index = self.number.index(max(self.number))
        mode = self.bins[index]
        return mode



    def getStDev(self):
        ''' computes the standard deviation of cell size in file and returns it'''
        mean = self.getMean()
        total = 0
        for i,bn in enumerate(self.bins):
            total = total + self.number[i]*(bn-mean)**2
        total = total/sum(self.number)
        stdev = (total)**0.5
        return stdev

    def getMedian(self):
        ''' Get the median of the data set '''
        tempList = []
        for i in range(len(self.number)):
            tempList = tempList + [self.bins[i]]*int(self.number[i])
        return np.median(tempList)

    def getMAD(self):
        '''Returns median absoloute deviation. It is a measure of spread robust to outliers and works for non normal distributions '''
        tempList = []
        for i in range(len(self.number)):
            tempList = tempList + [self.bins[i]]*int(self.number[i])
        return stats.median_absolute_deviation(tempList)


    def __str__(self):
        return str("Multisizer object with:",self.name,self.totalCount)

if __name__ == "__main__":
    import os
    import MultisizerReader
    import matplotlib
    import matplotlib.pyplot as plt

    #Get all spread sheet files in fodler and create multisizer files for each
    folder = "./Data_Organised/MG1655_GrowthCurve"
    allFiles = os.listdir(folder)
    multiSizerFiles = [allFiles[i] for i in range(len(allFiles)) if allFiles[i].endswith(".XLS")]
    data = []
    for files in multiSizerFiles:
        data.append(MultiSizerReader(path=os.path.join(folder,files)))

    #Extract ODs from file names
    ODList = [float(d.name.split("_")[2] +"."+ d.name.split("_")[3]) for d in data]

    #************************ PLOT EVERYTHING **********************************
    #Plotting all plots as individual traces
    MultiSizerReader.plotData(data,ODList,labels=["OD: {0} ".format(ODList[i]) for i in range(len(ODList))],legend=False,title="MG1655 size growth curve",joymode= False)
    #************************* Plot summed hists by OD *************************
    combinedData,combinedODs = MultiSizerReader.sumByGroup(data,ODList)
    MultiSizerReader.plotData(combinedData,combinedODs,labels=["OD: {0} ".format(combinedODs[i]) for i in range(len(combinedODs))],legend=True,alpha = 1.0,title = "MG1655 Summed cell size growth curve",joymode=False)
