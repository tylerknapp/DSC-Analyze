# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 10:57:09 2024

@author: tyler
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate

class DSCData:
    def __init__ (self, filepath):
        plt.ioff()
        # Basic Information
        self.filepath = filepath
        self.runs = self.read('runcount')
        self.steps = self.read('stepcount')
        self.data = self.read('data')
        self.sampleName = self.read('samplename')
        self.instrumentName = self.read('instrument')
        self.rundate = self.read('rundate')
        self.procedure = self.read('procedure')
        self.operator = self.read('operator')
        self.plotTitleTemp = self.sampleName
        self.plotTitleTime = self.sampleName
        
        # Conditionals
        self.scatter = False
        self.plotRun = 0
        self.analysisMode = True # True is Intersection, False is Integration
        
        # Plot Related
        self.fig1, self.axTemp = plt.subplots() # Create one figure, fig, with two subplots, axTemp and axTime
        self.fig2, self.axTime = plt.subplots()
        self.cid1 = None
        self.cid2 = None
        
        # Analysis Variables
        self.pointBank = []
        self.intersectPoints = {'m1': None, 'b1': None, 'm2': None, 'b2': None}
        self.linearLine = [0, 1]
        
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
                    
                    
                return dfNew
            
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
        

    def plot(self, x):
        try:
            if x == 'temp':
                if self.plotRun == 0:
                    
                    if self.scatter == False:
                        for i in range(0, self.runs):
                            self.axTemp.plot(self.data['Temp ' + str(i+1)], self.data['Heat ' + str(i+1)],
                                             picker = True, pickradius = 5)
                    else:
                        for i in range(0, self.runs):
                            self.axTemp.scatter(self.data['Temp ' + str(i+1)], self.data['Heat ' + str(i+1)],
                                             picker = True, pickradius = 5)
                else:
                    
                    if self.scatter == False:
                        self.axTemp.plot(self.data['Temp ' + str(self.plotRun)], self.data['Heat ' + str(self.plotRun)],
                                         picker = True, pickradius = 5)
                    else:
                        self.axTemp.scatter(self.data['Temp ' + str(self.plotRun)], self.data['Heat ' + str(self.plotRun)],
                                         picker = True, pickradius = 5)
                if __name__ == "__main__": self.fig1.show()

            elif x == 'time':
                if self.plotRun == 0:
                    
                    if self.scatter == False:
                        for i in range(0, self.runs):
                            self.axTime.plot(self.data['Time ' + str(i+1)], self.data['Heat ' + str(i+1)],
                                             picker = True, pickradius = 5)
                    else:
                        for i in range(0, self.runs):
                            self.axTime.scatter(self.data['Time ' + str(i+1)], self.data['Heat ' + str(i+1)],
                                             picker = True, pickradius = 5)
                else:
                    
                    if self.scatter == False:
                        self.axTime.plot(self.data['Time ' + str(self.plotRun)], self.data['Heat ' + str(self.plotRun)],
                                         picker = True, pickradius = 5)
                    else:
                        self.axTime.scatter(self.data['Time ' + str(self.plotRun)], self.data['Heat ' + str(self.plotRun)],
                                         picker = True, pickradius = 5)
                if __name__ == "__main__": self.fig2.show()
            
            self.axTemp.set_title(self.plotTitleTemp)
            self.axTime.set_title(self.plotTitleTime)
            self.axTemp.set_xlabel('Temperature (°C)')
            self.axTemp.set_ylabel('Heat Flow (W/g)')
            self.axTime.set_xlabel('Time (s)')
            self.axTime.set_ylabel('Heat Flow (W/g)')
            
            self.cid1 = self.fig1.canvas.mpl_connect('pick_event', self.onpick)
            self.cid2 = self.fig2.canvas.mpl_connect('pick_event', self.onpick)
            
        except Exception as error:
            print(error)


    def cleanPlot(self):
        self.fig1.clf()
        plt.close(self.fig1)
        self.fig1, self.axTemp = plt.subplots()
        
        self.fig2.clf()
        plt.close(self.fig2)
        self.fig2, self.axTime = plt.subplots()
        
        self.fig1.canvas.mpl_disconnect(self.cid1)
        self.fig2.canvas.mpl_disconnect(self.cid2)
        
        self.linearLine = [0, 1]
        
    def deletePlots(self):
        plt.close(self.fig1)
        plt.close(self.fig2)
        
    def onpick(self, event):
        thisline = event.artist
        xdata = thisline.get_xdata()
        ydata = thisline.get_ydata()
        ind = event.ind
        points = (xdata, ydata, ind)
        
        if self.analysisMode == True:
            self.intersectCalc(points)
        else:
            self.integrateCalc(points)
    
    def pointClean(self):
        self.pointBank = []
        self.intersectPoints = {'m1': None, 'b1': None, 'm2': None, 'b2': None}
    
    
    def intersectCalc(self, points):
        isTime = False
        if len(self.pointBank) == 4:
            self.pointClean()
            self.cleanPlot()
            self.plot('temp')
            self.plot('time')
        
        self.pointBank.append([points[0][0], points[1][0], points[2][0]])
        currentRun = self.plotRun
        
        if self.pointBank[0][0] - self.data['Time ' + str(currentRun)].iloc[self.pointBank[0][2]-1] == 0.2: isTime = True; print(isTime)
        if len(self.pointBank) == 2:
            if isTime == False:
                xlist = [x for x in self.data['Temp ' + str(currentRun)].iloc[self.pointBank[0][2]:self.pointBank[1][2]]]
                ylist = [y for y in self.data['Heat ' + str(currentRun)].iloc[self.pointBank[0][2]:self.pointBank[1][2]]]
                
                xArray = np.array(xlist)
                yArray = np.array(ylist)
                
                self.linearLine[0] = self.axTemp.plot(xlist, ylist)
                self.intersectPoints['m1'], self.intersectPoints['b1'] = self.linearreg(xArray, yArray)
            else:
                xlist = [x for x in self.data['Time ' + str(currentRun)].iloc[self.pointBank[0][2]:self.pointBank[1][2]]]
                ylist = [y for y in self.data['Heat ' + str(currentRun)].iloc[self.pointBank[0][2]:self.pointBank[1][2]]]
                
                xArray = np.array(xlist)
                yArray = np.array(ylist)
                
                self.linearLine[0] = self.axTime.plot(xlist, ylist)
                self.intersectPoints['m1'], self.intersectPoints['b1'] = self.linearreg(xArray, yArray)
            
            if isTime == False:
                self.fig1.canvas.draw()
            else:
                self.fig2.canvas.draw()
            
        if len(self.pointBank) == 4:
            if isTime == False:
                xlist = [x for x in self.data['Temp ' + str(currentRun)].iloc[self.pointBank[2][2]:self.pointBank[3][2]]]
                ylist = [y for y in self.data['Heat ' + str(currentRun)].iloc[self.pointBank[2][2]:self.pointBank[3][2]]]
                
                xArray = np.array(xlist)
                yArray = np.array(ylist)
                
                self.linearLine[1] = self.axTemp.plot(xlist, ylist)
                self.intersectPoints['m2'], self.intersectPoints['b2'] = self.linearreg(xArray, yArray)
            else:
                xlist = [x for x in self.data['Time ' + str(currentRun)].iloc[self.pointBank[2][2]:self.pointBank[3][2]]]
                ylist = [y for y in self.data['Heat ' + str(currentRun)].iloc[self.pointBank[2][2]:self.pointBank[3][2]]]
                
                xArray = np.array(xlist)
                yArray = np.array(ylist)
                
                self.linearLine[1] = self.axTime.plot(xlist, ylist)
                self.intersectPoints['m2'], self.intersectPoints['b2'] = self.linearreg(xArray, yArray)

            A = np.array([[1, -self.intersectPoints['m1']],[1, -self.intersectPoints['m2']]])
            Ay = np.array([[self.intersectPoints['b1'], -self.intersectPoints['m1']],[self.intersectPoints['b2'], -self.intersectPoints['m2']]])
            Ax = np.array([[1, self.intersectPoints['b1']],[1, self.intersectPoints['b2']]])
            
            detA = np.linalg.det(A)
            detAy = np.linalg.det(Ay)
            detAx = np.linalg.det(Ax)
            
            Inters = (detAx/detA, detAy/detA)
            
            if isTime == False:
                self.axTemp.text(Inters[0], Inters[1], Inters[0])
                self.fig1.canvas.draw()
            else:
                self.axTime.text(Inters[0], Inters[1], Inters[0])
                self.fig2.canvas.draw()
            
            
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
        self.pointBank.append(points)
        
        
    ### TESTING ###
            
if __name__ == "__main__":
    data = DSCData(r"D:\DSC\Naphthalene Ramping\Sample_10_31_23\105 M\Naphthalene Ramp 30 105M 25Q 10_31_23.csv")
    data.plotRun=1
    data.plot('temp')
    # data.plotRun = 0
    # data.plot(x = 'temp')