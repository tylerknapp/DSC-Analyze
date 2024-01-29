# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 10:57:09 2024

@author: tyler
Version 1.5
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.integrate as integrate

class DSCData:
    def __init__ (self, filepath):
        plt.ioff()
        # Basic Information
        self.filepath = filepath
        self.runs = self.read('runcount')
        self.steps = self.read('stepcount')
        self.rampRate = self.read('ramprate')
        self.data = self.read('data')
        self.sampleName = self.read('samplename')
        self.sampleMelt = None
        self.instrumentName = self.read('instrument')
        self.rundate = self.read('rundate')
        self.procedure = self.read('procedure')
        self.operator = self.read('operator')
        self.plotTitle = self.sampleName
        
        # Conditionals
        self.scatter = False
        self.plotRun = 0
        self.analysisMode = True # True is Intersection, False is Integration
        
        # Plot Related
        self.fig, self.ax = plt.subplots() # Create one figure, fig, with two subplots, axTemp and axTime
        self.cid = self.fig.canvas.mpl_connect('pick_event', self.onpick)
        self.plotType = ['Temp', 'Heat']
        
        # Analysis Variables
        self.pointBank = []
        self.intersectPoints = {'m1': None, 'b1': None, 'm2': None, 'b2': None}
        
    ### METHODS ###
    
    def read(self, locator):
        with open(self.filepath) as x:
            lines = x.readlines()
            if locator == 'data':
                cntBeg = 0
                cntEnd = 0
                begReached = False
                run = 1
                runCounter = 0
                dfRaw = pd.DataFrame()
                
                for i in range(0, len(lines)):

                    if lines[i] == 'Time,Temperature,Heat Flow (Normalized)\n' and begReached == False:
    
                        cntBeg = i+1
                        begReached = True
                        
                    if (lines[i] == "[step]\n" and begReached == True) or i+1 == len(lines):
    
                        cntEnd = i-2
                        labels = ["Time "+str(run), "Temp "+str(run), "Heat "+str(run)]
                        dfTemp = pd.read_csv(self.filepath, skiprows = cntBeg, nrows = cntEnd-cntBeg, header=0, names=labels)
                        dfTemp = dfTemp.dropna()
                        
                        dfRaw = pd.concat([dfRaw, dfTemp], axis=1)
                        begReached = False
                        runCounter += 1
                        
                        if runCounter == self.steps:
                            run += 1
                            runCounter = 0
                            
                dfStack = pd.DataFrame()
                newList = []
                labels = []
        
                
                for i in range(0, self.steps*self.runs+1):
        
                    dfTemp = dfRaw.iloc[:, i*3:i*3+3]
                    dfTemp = dfTemp.dropna()
                    if (i%(self.steps) != 0 or i == 0):
                        dfStack = pd.concat([dfStack, dfTemp])
                    else:
                        
                        for column in dfStack.columns:
                            li = dfStack[column].tolist()
                            newList.append(li)
                        dfStack = pd.DataFrame()
                        dfStack = pd.concat([dfStack, dfTemp])
                    if i == self.steps*self.runs:
                        dfStack = pd.concat([dfStack, dfTemp])
                    
                for i in range(0, self.runs):
                    labels.extend(["Time "+str(i+1), "Temp "+str(i+1), "Heat "+str(i+1)])
                        
        
                indexMax = len(max(newList, key=len))
                dfNew = pd.DataFrame(index = range(0, indexMax))

                for i in labels:
                    dfNew[i] = pd.Series(newList[labels.index(i)])

                for i in range(1, self.runs):
                    dfNew['Time ' + str(i+1)] = dfNew['Time ' + str(i+1)] - dfNew['Time ' + str(i+1)].iloc[0]
                    
                    
                return self.rampCalc(dfNew)
            
            elif locator == 'operator':
                return lines[2].removeprefix('Operator,')
            elif locator == 'samplename':
                return lines[4].removeprefix('Sample name,')
            elif locator == 'instrument':
                return lines[1].removeprefix('Instrument name,')
            elif locator == 'rundate':
                return lines[3].removeprefix('rundate,')
            elif locator == 'procedure':
                return lines[5].removeprefix('proceduresegments,')
            elif locator == 'runcount':
                text = lines[5]
                text = text[text.index('Repeat'):]
                textList = text.split()
                return 1 + int(textList[1]) * int(textList[3])
            elif locator == 'stepcount':
                text = lines[5]
                text = text[text.index('Data On'):text.index('Data Off')]
                textList = text.split(';')
                return len(textList)-2
            elif locator == 'ramprate':
                text = lines[7]
                textList = text.split()
                return int(textList[1])
        

    def rampCalc(self, df):
        for i in range(1, self.runs+1):
            diffList = [None]
            for j, x in enumerate(df['Temp ' + str(i)]):
                if j == 0:
                    continue
                else:
                    diffList.append(((df['Temp ' + str(i)].iloc[j]-df['Temp ' + str(i)].iloc[j-1])/0.1)*60)
            df['Temp Diff ' + str(i)] = diffList
        
        return df
        
    def plot(self):
        try:
            if self.plotRun == 0:
                
                if self.scatter == False:
                    for i in range(0, self.runs):
                        self.ax.plot(self.data[self.plotType[0] + ' ' + str(i+1)], self.data[self.plotType[1] + ' ' + str(i+1)],
                                         picker = True, pickradius = 2)
                else:
                    for i in range(0, self.runs):
                        self.ax.scatter(self.data[self.plotType[0] + ' ' + str(i+1)], self.data[self.plotType[1] + ' ' + str(i+1)],
                                         picker = True, pickradius = 2)
            else:
                
                if self.scatter == False:
                    self.ax.plot(self.data[self.plotType[0] + ' ' + str(self.plotRun)], self.data[self.plotType[1] + ' ' + str(self.plotRun)],
                                     picker = True, pickradius = 2)
                else:
                    self.ax.scatter(self.data[self.plotType[0] + ' ' + str(self.plotRun)], self.data[self.plotType[1] + ' ' + str(self.plotRun)],
                                     picker = True, pickradius = 2)
            if __name__ == "__main__": self.fig.show()

            
            self.ax.set_title(self.plotTitle)
            if self.plotType[0] == 'Temp': self.ax.set_xlabel('Temperature (°C)')
            else: self.ax.set_xlabel('Time (s)')
            if self.plotType[1] == 'Heat': self.ax.set_ylabel('Heat Flow (W/g)')
            elif self.plotType[1] == 'Temp': self.ax.set_ylabel('Temperature (°C)')
            else: self.ax.set_ylabel('Ramp Rate (°C/min)')
            
            self.cid = self.fig.canvas.mpl_connect('pick_event', self.onpick)
            
        except Exception as error:
            print(error)


    def cleanPlot(self):
        plt.cla()
        self.pointBank = []
        self.intersectPoints = {'m1': None, 'b1': None, 'm2': None, 'b2': None}
        
    def deletePlots(self):
        plt.close('all')
        
    def onpick(self, event):
        if (len(self.pointBank) == 4 and self.analysisMode == True) or (len(self.pointBank) == 2 and self.analysisMode == False):
            self.cleanPlot()
            self.plot()

        thisline = event.artist
        xdata = thisline.get_xdata()
        ydata = thisline.get_ydata()
        ind = event.ind
        points = (xdata, ydata, ind)

        self.ax.text(self.data[self.plotType[0] + ' ' + str(self.plotRun)].iloc[ind[0]], 
                     self.data['Heat ' + str(self.plotRun)].iloc[ind[0]],
                     self.data[self.plotType[0] + ' ' + str(self.plotRun)].iloc[ind[0]])
        self.fig.canvas.draw()
        
        if self.analysisMode == True:
            self.intersectCalc(points)
        else:
            self.integrateCalc(points)
    
    
    def intersectCalc(self, points):

        try:
            self.pointBank.append([points[0][0], points[1][0], points[2][0]])
            cRun = self.plotRun
            
            # Get first linear line
            if len(self.pointBank) == 2:
                
                xlist = [x for x in self.data[self.plotType[0] + ' ' + str(cRun)].iloc[self.pointBank[0][2]:self.pointBank[1][2]]]
                ylist = [y for y in self.data[self.plotType[1] + ' ' + str(cRun)].iloc[self.pointBank[0][2]:self.pointBank[1][2]]]
                
                xArray = np.array(xlist)
                yArray = np.array(ylist)
                
                self.ax.plot(xlist, ylist)
                self.intersectPoints['m1'], self.intersectPoints['b1'] = self.linearreg(xArray, yArray)
                
                
                self.fig.canvas.draw()
                
            # Get second linear line
            if len(self.pointBank) == 4:
                xlist = [x for x in self.data[self.plotType[0] + ' ' + str(cRun)].iloc[self.pointBank[2][2]:self.pointBank[3][2]]]
                ylist = [y for y in self.data[self.plotType[1] + ' ' + str(cRun)].iloc[self.pointBank[2][2]:self.pointBank[3][2]]]
                
                xArray = np.array(xlist)
                yArray = np.array(ylist)
                
                self.ax.plot(xlist, ylist)
                self.intersectPoints['m2'], self.intersectPoints['b2'] = self.linearreg(xArray, yArray)
    
                # Find the intersection of the two lines
                A = np.array([[1, -self.intersectPoints['m1']],[1, -self.intersectPoints['m2']]])
                Ay = np.array([[self.intersectPoints['b1'], -self.intersectPoints['m1']],[self.intersectPoints['b2'], -self.intersectPoints['m2']]])
                Ax = np.array([[1, self.intersectPoints['b1']],[1, self.intersectPoints['b2']]])
                
                detA = np.linalg.det(A)
                detAy = np.linalg.det(Ay)
                detAx = np.linalg.det(Ax)
                
                Inters = (detAx/detA, detAy/detA)
                
                # Place text at intersection
                self.ax.text(0, 1, 'Intersection: ' + str(Inters[0]), transform = self.ax.transAxes)
                self.fig.canvas.draw()
        except Exception as error:
            print(error)
            self.cleanPlot()
            self.plot()
            self.fig.canvas.draw()
            
    def linearreg(self, x, y):
        #Number of points
    
        n = np.size(x)
        
        #Find mean of x and y
        m_x=np.mean(x)
        m_y=np.mean(y)
        
        #Calculate cross deviation and deviation about x
        SS_xy = np.sum(y*x) - n*m_y*m_x
        SS_xx = np.sum(x*x) - n*m_x*m_x
        
        #Calculate regression coefficients
        m = SS_xy / SS_xx
        b = m_y - m*m_x
        
        return(m, b)
        
    def integrateCalc(self, points):
        try:
                 
            self.pointBank.append([points[0][0], points[1][0], points[2][0]])
            cRun = self.plotRun
            
            if len(self.pointBank) == 2:
                xlist = [x for x in self.data[self.plotType[0] + ' ' + str(cRun)].iloc[self.pointBank[0][2]:self.pointBank[1][2]]]
                ylist = [y for y in self.data[self.plotType[1] + ' ' + str(cRun)].iloc[self.pointBank[0][2]:self.pointBank[1][2]]]
                
                xArray = np.array(xlist)
                yArray = np.array(ylist)
                
                self.ax.plot(xlist, ylist)
                
                Heat = integrate.simpson(yArray, xArray)
                if self.plotType == ['Temp', 'Heat']: Heat = Heat / (self.rampRate / 60)
                self.ax.text(0, 1, 'Heat: ' + str(Heat), transform = self.ax.transAxes)
                self.fig.canvas.draw()
            
        except Exception as error:
            print(error)
            self.cleanPlot()
            self.plot()
            self.fig.canvas.draw()
        
    def autoNucTime(self, run):
        
        ind = None
        for i in range(len(self.data)):
            if i == 0:
                continue
            else:
                if self.data.iloc[i, 1+(run-1)*3] <= self.sampleMelt and self.data.iloc[i-1, 1+(run-1)*3] >= self.sampleMelt:
                    
                    ind = i
                    break
        xRaw = self.data.iloc[ind:, (run-1)*3].tolist()
        
        x = [a - xRaw[0] for a in xRaw]
        y = self.data.iloc[ind:, 1+(run-1)*3].tolist()
        
        dydx = np.diff(y)/np.diff(x)
        x.pop(-1)
        
        dy2d2x = np.diff(dydx)/np.diff(x)
        return round(x[np.where(dy2d2x == min(dy2d2x))[0][0]], 1)
    
    ### TESTING ###
            
if __name__ == "__main__":
    data = DSCData(r"D:\DSC\Naphthalene Ramping\Sample_10_31_23\105 M\Naphthalene Ramp 30 105M 25Q 10_31_23.csv")
    # data.plotRun=1
    # data.plot('temp')
    # data.plotRun = 0
    # data.plot(x = 'temp')