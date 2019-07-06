import os
import numpy as np
import matplotlib
matplotlib.rcParams["savefig.directory"] = os.chdir(os.path.dirname(__file__))
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import seaborn as sns



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
        xLims=None,logNormalFits=False):
        '''
        Should plot joy like plots for all multisizer objects in list "dataList". Will color traces with same group value the same color
        '''
        spacing = smoothing*spacing
        if joymode == True:
            plt.style.use("dark_background")
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
            y = ((np.asarray(Y))/sum(Y)) + spacing*i
            y2 = [spacing*i for k in range(len(X))]

            if i != len(dataList)-1:
                if groupValues[i] != groupValues[i+1]:
                    c = c - 1

            #Draw fill between black line and new zero line and fit log normal
            plt.fill_between(x,y,y2, step="pre", alpha=alpha,color=colors[c], zorder = zorder[i], label=str(labels[i])+'N: {0}k'.format(int(dataList[i].totalCount/1000.0)))
            if logNormalFits == True:
                logNormalX,logNormalY, mu, sigma = MultiSizerReader.fitLogNormal(x,y-spacing*(i))

                plt.plot(logNormalX,logNormalY+spacing*i,"b",zorder=zorder[i],label = "Median: {}".format(np.exp(mu)))
                plt.legend


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
                plt.fill_between([x[medianIndex],x[medianIndex+1]],[y[medianIndex],y[medianIndex+1]],[y2[medianIndex],y2[medianIndex+1]], step="pre", alpha=alpha,color="k",zorder=zorder[i])

            if joymode == True:
                lineColor = "w"
            if joymode == False:
                lineColor = 'k'
            #Plot black line on top of hist
            plt.plot(x,y,color=lineColor,drawstyle="steps",zorder =zorder[i] )
            if legend == True:
                plt.legend()
            elif legend == False:
                plt.text(lowerXLim + (upperXLim-lowerXLim)*0.6, y[-1]+0.001, str(labels[i]) + 'N: {0}k'.format(int(dataList[i].totalCount/1000.0)))

        plt.gcf().set_size_inches(12, 8 )
        for item in ([plt.gcf().get_axes()[0].title,plt.gcf().get_axes()[0].xaxis.label, plt.gcf().get_axes()[0].yaxis.label]
            + plt.gcf().get_axes()[0].get_xticklabels() + plt.gcf().get_axes()[0].get_yticklabels()):
            item.set_fontsize(20)
        if logAxis:
            plt.xscale("log")
            plt.gcf().get_axes()[0].set_xticks([0.2, 0.5,0.7, 1.0,2.0,4.0,6.0,8.0,10])
        plt.gcf().get_axes()[0].xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
        plt.xlabel("Volume $\mu m^3$")
        plt.ylabel("Relative Normalised Count")
        if title != None:
            plt.gcf().get_axes()[0].set_title(title,fontsize=20)
        plt.xlim(lowerXLim,upperXLim)
        plt.show()

    def boxPlotData(dataList,groupValues = None, labels= None, title=None,positions=None):
        '''
        Plot box plot of data coloring boxes by group color
        '''

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

        boxData = [boxData[i]/np.mean(boxData[0]) for i in range(len(boxData))]
        bp = plt.boxplot(boxData,labels=labels,vert=True,sym='.',whis=[1,99],patch_artist=True,showmeans=True,positions=positions)
        plt.violinplot(boxData, points=300, widths=1.0, vert=True,
                      showmeans=False, showextrema=False, showmedians=False,positions=positions)
        plt.plot([0,4,5,6],[4.6/4.6,3.8/4.6,3.9/4.6,3.5/4.6],'v--',zorder=999)


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

        plt.gcf().set_size_inches(12, 8 )
        for item in ([plt.gcf().get_axes()[0].title,plt.gcf().get_axes()[0].xaxis.label, plt.gcf().get_axes()[0].yaxis.label]
            + plt.gcf().get_axes()[0].get_xticklabels() ):
            item.set_fontsize(20)
        plt.xlabel("Concentration of extra NaCl (mM)")
        plt.ylabel("Volume $\mu m^3$")
        if title != None:
            plt.gcf().get_axes()[0].set_title(title,fontsize=20)
        plt.yticks(fontsize=20,rotation = 50);
        plt.tight_layout()
        plt.show()

    def sumByGroup(dataList,groupValues,labels=None):
        '''
        Compiles multiple Multisizers files by summing their bins if they have the same groupValue. Size of lists "dataList" and "goupValues" should be the same
        '''
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
        index = 0
        done = False
        while not done:

            if index+binsToSmooth > len(bins) -1 :
                #Have some remainder left
                done = True
                newBins.append(bins[index])
                newHeights.append(sum(heights[index:index + (len(bins)-1-index)]))
            else:
                newBins.append(bins[index])
                newHeights.append(sum(heights[index:index+binsToSmooth]))
            index = index +  binsToSmooth
            #Perfectly fit into range
            if index == len(bins) -1:
                done = True
        return newBins, newHeights

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
