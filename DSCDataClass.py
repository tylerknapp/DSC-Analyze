# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 12:28:17 2023
version 1.3
@author: tyler
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate
        
class DSCData:
    def __init__ (self, filepath, runs, steps):
        plt.ioff()
        # Core functionality properties
        self.filepath = filepath
        self.runs = runs
        self.steps = steps
        self.data = self.read('data')
        self.fig, self.ax = plt.subplots()
        # Variable Deciders
        self.pickerType = "Point"
        
        # Information properties
        self.samplename = self.read('samplename')
        self.instrumentname = self.read('instrument')
        self.rundate = self.read('rundate')
        self.procedure = self.read('procedure')
        self.operator = self.read('operator')
        self.data = self.read('data')
        self.rampRate = 1
        
        # # Figure formatting properties
        # self.ax.set_title(self.samplename)
        # self.ax.set_xlabel('Temperature (°C)')
        # self.ax.set_ylabel('Heat (W/g)')
        
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
                    # if i == 104: breakpoint()
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
    
    def cleanPlot(self):
        self.fig.clf()
        plt.close(self.fig)
        self.fig, self.ax = plt.subplots()
        self.lin = [0]*self.runs
        self.linearLin = [0, 1]
        self.cid = None
        self.clickCount = 0
        self.linIndex = []
        self.pickRun = 1
        self.ax.set_title(self.samplename)
        self.ax.set_xlabel('Temperature (°C)')
        self.ax.set_ylabel('Heat (W/g)')
        
    
    def plot(self, run, scatter=False):
        self.cleanPlot()
        if run !=0:
            self.cid = self.fig.canvas.mpl_connect("pick_event", self.picker)
            self.pickRun = run
            if scatter==False:
                self.lin = None
                self.lin, = self.ax.plot(self.data['Temp '+str(run)], self.data['Heat '+str(run)],
                                     picker=True, pickradius=5)
                # self.fig.show()
            else:
                self.lin = None
                self.lin = self.ax.scatter(self.data['Temp '+str(run)], self.data['Heat '+str(run)],
                                     picker=True, pickradius=5)
                # self.fig.show()
            
        else:
            try:
                self.fig.canvas.mpl_disconnect(self.cid)
            except:
                pass
            if scatter==False:
                self.lin = [0]*self.runs
                for i in range(0, self.runs):
                    self.lin[i] = self.ax.plot(self.data['Temp '+str(i+1)], self.data['Heat '+str(i+1)])
                # self.fig.show()
            else:
                self.lin = [0]*self.runs
                for i in range(0, self.runs):
                    self.lin[i] = self.ax.scatter(self.data['Temp '+str(i+1)], self.data['Heat '+str(i+1)])
                # self.fig.show()
            
    def picker(self, event):
        if self.pickerType == "Point":
            for txt in self.ax.texts:
                txt.set_visible(False)
                
            if self.clickCount == -1:
                self.clickCount=0
                self.linIndex=[]
                self.linearLin[0].pop(0).remove()
                self.linearLin[1].pop(0).remove()
                
            if self.clickCount >= 0 and self.clickCount < 4:
                ind=event.ind
                # print(ind)
                self.clickCount=self.clickCount+1
                self.linIndex.append(ind[-1])
                print('Index of point:', ind[0])
                self.ax.text(self.data.iloc[ind[0], 3*self.pickRun-2], 
                             self.data.iloc[ind[0], 3*self.pickRun-1],
                             self.data.iloc[ind[0], 3*self.pickRun-2])
                self.fig.canvas.draw()
                
            if self.clickCount == 4:
                for txt in self.ax.texts:
                    txt.set_visible(False)
                try:
                    line1dat = [self.data.iloc[self.linIndex[0]:self.linIndex[1]+1, 3*self.pickRun-2], 
                                     self.data.iloc[self.linIndex[0]:self.linIndex[1]+1, 3*self.pickRun-1]]
                    line2dat = [self.data.iloc[self.linIndex[2]:self.linIndex[3]+1, 3*self.pickRun-2], 
                                     self.data.iloc[self.linIndex[2]:self.linIndex[3]+1, 3*self.pickRun-1]]
                    
                    self.linearLin[0] = self.ax.plot(line1dat[0], line1dat[1], color='r')
                    self.linearLin[1] = self.ax.plot(line2dat[0], line2dat[1], color='orange')
                    
                    # print(self.line1dat)
                    self.fig.canvas.draw()
                except Exception as error:
                    print("Error in picking: ", error)
                    self.clickCount=-1
                    self.linIndex=[]
                    return
                    
                try:
                    m1, b1 = self.linearreg(self.data.iloc[self.linIndex[0]:self.linIndex[1], 3*self.pickRun-2],
                                       self.data.iloc[self.linIndex[0]:self.linIndex[1], 3*self.pickRun-1])
                    m2, b2 = self.linearreg(self.data.iloc[self.linIndex[2]:self.linIndex[3], 3*self.pickRun-2],
                                       self.data.iloc[self.linIndex[2]:self.linIndex[3], 3*self.pickRun-1])
                except Exception as error:
                    print("Error in linear regression: ", error)
                    self.clickCount=-1
                    self.linIndex=[]
                    return
                
                try:
                    A = np.array([[1, -m1],[1, -m2]])
                    Ay = np.array([[b1, -m1],[b2, -m2]])
                    Ax = np.array([[1, b1],[1, b2]])
                    
                    detA = np.linalg.det(A)
                    detAy = np.linalg.det(Ay)
                    detAx = np.linalg.det(Ax)
                    
                    Inters = (detAx/detA, detAy/detA)
                    
                    print(Inters)
                    self.ax.text(Inters[0], Inters[1], Inters[0])
                    self.fig.canvas.draw()
                except Exception as error:
                    print("Error in intersection calculation: ", error)
                    self.clickCount=-1
                    self.linIndex=[]
                    return
                
                self.clickCount=-1
                self.linIndex=[]
            else:
                for txt in self.ax.texts:
                    txt.set_visible(False)
                    
                if self.clickCount == -1:
                    self.clickCount=0
                    self.linIndex=[]
                    self.linearLin[0].pop(0).remove()
                    self.linearLin[1].pop(0).remove()
                    
                if self.clickCount >= 0 and self.clickCount < 2:
                    ind=event.ind
                    # print(ind)
                    self.clickCount=self.clickCount+1
                    self.linIndex.append(ind[-1])
                    print('Index of point:', ind[0])
                    self.ax.text(self.data.iloc[ind[0], 3*self.pickRun-2], 
                                 self.data.iloc[ind[0], 3*self.pickRun-1],
                                 self.data.iloc[ind[0], 3*self.pickRun-2])
                    self.fig.canvas.draw()
                    
                if self.clickCount == 2:
                    for txt in self.ax.texts:
                        txt.set_visible(False)
                    try:
                        line1dat = [self.data.iloc[self.linIndex[0]:self.linIndex[1]+1, 3*self.pickRun-2], 
                                         self.data.iloc[self.linIndex[0]:self.linIndex[1]+1, 3*self.pickRun-1]]
                        # line2dat = [self.data.iloc[self.linIndex[2]:self.linIndex[3]+1, 3*self.pickRun-2], 
                                         # self.data.iloc[self.linIndex[2]:self.linIndex[3]+1, 3*self.pickRun-1]]
                        
                        self.linearLin[0] = self.ax.plot(line1dat[0], line1dat[1], color='r')
                        # self.linearLin[1] = self.ax.plot(line2dat[0], line2dat[1], color='orange')
                        
                        # print(self.line1dat)
                        self.fig.canvas.draw()
                    except Exception as error:
                        print("Error in picking: ", error)
                        self.clickCount=-1
                        self.linIndex=[]
                        return
                    try:
                        ylist = [x for x in self.data.iloc[self.linIndex[0]:self.linIndex[1]+1, 3*self.pickRun-1]]
                        ydata = np.array(ylist)
                        xlist = [x for x in self.data.iloc[self.linIndex[0]:self.linIndex[1]+1, 3*self.pickRun-3]]
                        xdata = np.array(xlist)
                        
                        area = integrate.simpson(y = ydata, x = xdata)
                        heatCapacity = area/self.rampRate
                        
                        self.ax.text(heatCapacity, 0, 0)
                        self.fig.canvas.draw()
                        
                    except Exception as error:
                        print("Error in integration: ", error)
                        self.clickCount=-1
                        self.linIndex=[]
                        return
                    self.clickCount = -1
                    self.linIndex=[]
                    
                    # try:
                    #     m1, b1 = self.linearreg(self.data.iloc[self.linIndex[0]:self.linIndex[1], 3*self.pickRun-2],
                    #                        self.data.iloc[self.linIndex[0]:self.linIndex[1], 3*self.pickRun-1])
                    #     m2, b2 = self.linearreg(self.data.iloc[self.linIndex[2]:self.linIndex[3], 3*self.pickRun-2],
                    #                        self.data.iloc[self.linIndex[2]:self.linIndex[3], 3*self.pickRun-1])
                    # except Exception as error:
                    #     print("Error in linear regression: ", error)
                    #     self.clickCount=-1
                    #     self.linIndex=[]
                    #     return
                    
                    # try:
                    #     A = np.array([[1, -m1],[1, -m2]])
                    #     Ay = np.array([[b1, -m1],[b2, -m2]])
                    #     Ax = np.array([[1, b1],[1, b2]])
                        
                    #     detA = np.linalg.det(A)
                    #     detAy = np.linalg.det(Ay)
                    #     detAx = np.linalg.det(Ax)
                        
                    #     Inters = (detAx/detA, detAy/detA)
                        
                    #     print(Inters)
                    #     self.ax.text(Inters[0], Inters[1], Inters[0])
                    #     self.fig.canvas.draw()
                    # except Exception as error:
                    #     print("Error in intersection calculation: ", error)
                    #     self.clickCount=-1
                    #     self.linIndex=[]
                    #     return
                    
                    # self.clickCount=-1
                    # self.linIndex=[]
    
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
    
    def NucTime(self, run):

        ind = None
        for i in range(len(self.data)):
            if i == 0:
                continue
            else:

                if self.data.iloc[i, 1+(run-1)*3] <= 80 and self.data.iloc[i-1, 1+(run-1)*3] >= 80:

                    ind = i
                    break
        xRaw = self.data.iloc[ind:, 0+(run-1)*3].tolist()
        
        x = [a - xRaw[0] for a in xRaw]
        y = self.data.iloc[ind:, 1+(run-1)*3].tolist()

        dydx = np.diff(y)/np.diff(x)
        x.pop(-1)
      
        dy2d2x = np.diff(dydx)/np.diff(x)
        return x[np.where(dy2d2x == min(dy2d2x))[0][0]]

        
        
if __name__ == "__main__":
    data = DSCData(r"D:\DSC\Naphthalene Ramping\Sample_10_31_23\105 M\Naphthalene Ramp 30 105M 25Q 10_31_23.csv",
                     3, 3)
    # print(data.NucTime(1))
    data.plot(run=0, scatter=False)
    # data.rampRate = 30
    # data.pickType = "Integrate"