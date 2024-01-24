# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 12:32:31 2024

@author: tyler
"""

import sys
import os
script_directory = os.path.realpath(os.path.dirname(__file__))
sys.path.append(script_directory)
import DSCDataClass2 as DC
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.pyplot import close

# Variables
data = None
# Functions
def submitPath():
    global data
    try:
        path = ePath.get()
        
        if path[0] == r'"':
            path = path[1:]
        if path[-1] == r'"':
            path = path[:-1]

        data = DC.DSCData(path)
        
    except Exception as error:
        tk.messagebox.showinfo("Error: ", error)

def plotData():
    global data
    
    if bPlot.cget('text') == 'Update': data.cleanPlot()

    tempTitle = eTempTitle.get()
    timeTitle = eTimeTitle.get()
    if tempTitle != False: data.plotTitleTemp = tempTitle
    if timeTitle != False: data.plotTitleTime = timeTitle

    data.plotRun = int(eRun.get())

    # Temp Plot
    data.plot('temp')
    
    canvasTemp = FigureCanvasTkAgg(data.fig1, master = tabTemp)
    
    canvasTemp.draw()
    
    canvasTemp.get_tk_widget().grid(row = 1, column = 2, rowspan = 20)
    
    
    
    toolbar_frameTemp = tk.Frame(master = tabTemp)
    toolbar_frameTemp.grid(row = 21, column = 2)
    
    toolbarTemp = NavigationToolbar2Tk(canvasTemp, toolbar_frameTemp)
    toolbarTemp.update()
    
    # Time Plot
    data.plot('time')
    
    canvasTime = FigureCanvasTkAgg(data.fig2, master = tabTime)
    
    canvasTime.draw()
    
    canvasTime.get_tk_widget().grid(row = 1, column = 2, rowspan = 20)
    
    
    
    toolbar_frameTime = tk.Frame(master = tabTime)
    toolbar_frameTime.grid(row = 21, column = 2)
    
    toolbarTime = NavigationToolbar2Tk(canvasTime, toolbar_frameTime)
    toolbarTime.update()

    # Update Button Text
    bPlot.config(text = 'Update')

def on_closing():
    data.deletePlots()
    close(data.fig1)
    close(data.fig2)
    
def swapScatter():
    data.scatter = not data.scatter
    
def intersectIntegrate():
    global data
    data.analysisMode = not data.analysisMode
    
    if bIntersectIntegrate.cget('text') == 'Intersect':
        bIntersectIntegrate.config(text = 'Integrate')
        lIntersectIntegrate.config(text = 'Integration\nActive')
    else:
        bIntersectIntegrate.config(text = 'Intersect')
        lIntersectIntegrate.config(text = 'Intersection\nActive')

# Structure
root = tk.Tk()
root.title("DSC Analyze")

# Tabs
Controls = ttk.Notebook(root)
Graphs = ttk.Notebook(root)

tabSettings = ttk.Frame(Controls)
tabPlotting = ttk.Frame(Controls)
tabTemp = ttk.Frame(Graphs)
tabTime = ttk.Frame(Graphs)

Controls.add(tabSettings, text='File Settings')
Controls.add(tabPlotting, text='Plotting')
Graphs.add(tabTemp, text='Heat Temperature')
Graphs.add(tabTime, text='Heat Time')

Controls.pack(expand=1, fill='both')
Graphs.pack(expand=1, fill='both')

# Settings Tab
lPath = tk.Label(tabSettings, text = 'File Path:')
lPath.grid(row = 0, column = 0, sticky = tk.W, pady = 2)
ePath = tk.Entry(tabSettings)
ePath.grid(row = 0, column = 1, columnspan = 3, stick = tk.W+tk.E, pady = 2)

bSubmit = tk.Button(tabSettings, text = 'Submit File Path', command = submitPath)
bSubmit.grid(row = 0, column = 4, sticky = tk.W, pady = 2)

# Plotting Tab
bPlot = tk.Button(tabPlotting, text = 'Plot', command = plotData)
bPlot.grid(row = 0, rowspan = 2, column = 0, sticky = tk.W, pady = 2)

lTempTitle = tk.Label(tabPlotting, text = 'Temp Plot\nTitle')
lTempTitle.grid(row = 0, column = 1, sticky = tk.W, pady = 2)
eTempTitle = tk.Entry(tabPlotting)
eTempTitle.grid(row = 1, column = 1, sticky = tk.W, pady = 2)

lTimeTitle = tk.Label(tabPlotting, text = 'Time Plot\nTitle')
lTimeTitle.grid(row = 0, column = 2, sticky = tk.W, pady = 2)
eTimeTitle = tk.Entry(tabPlotting)
eTimeTitle.grid(row = 1, column = 2, sticky = tk.W, pady = 2)

lScatter = tk.Label(tabPlotting, text = 'Scatter?')
lScatter.grid(row = 0, column = 3, sticky = tk.W, pady = 2)
chScatter = tk.Checkbutton(tabPlotting, command = swapScatter)
chScatter.grid(row = 1, column = 3, sticky = tk.W, pady = 2)

lRun = tk.Label(tabPlotting, text = 'Run Number\n0 plots all')
lRun.grid(row = 0, column = 4, sticky = tk.W, pady = 2)
eRun = tk.Entry(tabPlotting)
eRun.insert(0, '0')
eRun.grid(row = 1, column = 4, sticky = tk.W, pady = 2)

lIntersectIntegrate = tk.Label(tabPlotting, text = 'Intersection\nActive')
lIntersectIntegrate.grid(row = 0, column = 5, sticky = tk.W, pady = 2)
bIntersectIntegrate = tk.Button(tabPlotting, text = 'Intersect', command = intersectIntegrate)
bIntersectIntegrate.grid(row = 1, column = 5, sticky = tk.W, pady = 2)
