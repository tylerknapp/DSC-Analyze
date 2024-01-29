# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 12:32:31 2024

@author: tyler
Version: 1.5
"""

from Modules import DSCDataClass as DC
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.pyplot import close

def main():
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
            bSubmit['state'] = 'disabled'
                
        except Exception as error:
            tk.messagebox.showinfo("Error: ", error)
    
    def progRestart():
        root.destroy()
        main()
    
    def plotData():
        global data
        
        if bPlot.cget('text') == 'Update':
            data.cleanPlot()
            
    
        tempTitle = eTitle.get()
        if tempTitle != '': data.plotTitle = tempTitle
    
    
        data.plotRun = int(eRun.get())
    
        # Temp Plot
        data.plot()
        
        if bPlot.cget('text') == 'Plot':
            canvasTemp = FigureCanvasTkAgg(data.fig, master = root)
            
            canvasTemp.draw()
            
            canvasTemp.get_tk_widget().pack(expand = 1, fill = 'both')
            
            
            
            toolbar_frameTemp = tk.Frame(master = root)
            toolbar_frameTemp.pack(expand = 1, fill = 'both')
            
            toolbarTemp = NavigationToolbar2Tk(canvasTemp, toolbar_frameTemp)
            toolbarTemp.update()
            bPlot.config(text = 'Update')
            
        
        data.fig.canvas.draw()
        # Update Button Text
        
    
    def on_closing():
        close(all)
        
    def swapScatter():
        global data
        data.scatter = not data.scatter
    
    def swapTimeTemp(selection):
        global data
        if selection == 'Temperature':
            data.plotType = ['Temp', 'Heat']
        elif selection == 'Time':
            data.plotType = ['Time', 'Heat']
        elif selection == 'Time/Temperature':
            data.plotType = ['Time', 'Temp']
        elif selection == 'Time/dT':
            data.plotType = ['Time', 'Temp Diff']
    
    def intersectIntegrate():
        global data
        data.analysisMode = not data.analysisMode
        
        if bIntersectIntegrate.cget('text') == 'Intersect':
            bIntersectIntegrate.config(text = 'Integrate')
            lIntersectIntegrate.config(text = 'Intersection\nActive')
        else:
            bIntersectIntegrate.config(text = 'Intersect')
            lIntersectIntegrate.config(text = 'Integration\nActive')
    
    def autoNucTime():
        global data
        try:
            data.sampleMelt = int(eMelt.get())
            times = [str(data.autoNucTime(x)) + '\n' for x in range(1, data.runs+1)]
            delim = '\n'
            
            strTimes = delim.join([str(ele) for ele in times])
            messagebox.showinfo('Auto-Generated Nucleation Times', strTimes)
        except Exception as error:
            messagebox.showinfo('Error', str(error) + '\n\nOr invalid melting point was entered.')
    
    # Structure
    root = tk.Tk()
    root.title("DSC Analyze")
    
    # Tabs
    Controls = ttk.Notebook(root)
    
    tabSettings = ttk.Frame(Controls)
    tabPlotting = ttk.Frame(Controls)
    
    Controls.add(tabSettings, text='File Settings')
    Controls.add(tabPlotting, text='Plotting')
    
    Controls.pack(expand=1, fill='both')
    
    # Settings Tab
    lPath = tk.Label(tabSettings, text = 'File Path:')
    lPath.grid(row = 0, column = 0, pady = 2)
    ePath = tk.Entry(tabSettings)
    ePath.grid(row = 0, column = 1, columnspan = 3, stick = tk.W+tk.E, pady = 2)
    
    bSubmit = tk.Button(tabSettings, text = 'Submit File Path', command = submitPath)
    bSubmit.grid(row = 0, column = 4, pady = 2)
    
    lRestart = tk.Label(tabSettings, text = 'Restart with new file:')
    lRestart.grid(row = 1, column = 0, pady = 2)
    bRestart = tk.Button(tabSettings, text = 'Restart', command = progRestart)
    bRestart.grid(row = 1, column = 1, pady = 2)
    
    # Plotting Tab
    bPlot = tk.Button(tabPlotting, text = 'Plot', command = plotData)
    bPlot.grid(row = 0, rowspan = 2, column = 0, pady = 2)
    
    lPlotType = tk.Label(tabPlotting, text = 'Plot Type')
    lPlotType.grid(row = 0, column = 1, pady = 2, padx = 50)
    plotDefault = tk.StringVar(tabPlotting)
    
    drPlotType = tk.OptionMenu(tabPlotting, plotDefault, 'Temperature', 'Time', 'Time/Temperature', 'Time/dT', command = swapTimeTemp)
    drPlotType.grid(row = 1, column = 1, pady = 2)
    plotDefault.set('Temperature')
    
    lTitle = tk.Label(tabPlotting, text = 'Plot Title')
    lTitle.grid(row = 0, column = 2, pady = 2)
    eTitle = tk.Entry(tabPlotting)
    eTitle.grid(row = 1, column = 2, pady = 2)
    
    lScatter = tk.Label(tabPlotting, text = 'Scatter?')
    lScatter.grid(row = 0, column = 3, pady = 2)
    chScatter = tk.Checkbutton(tabPlotting, command = swapScatter)
    chScatter.grid(row = 1, column = 3, pady = 2)
    
    lRun = tk.Label(tabPlotting, text = 'Run Number\n0 plots all')
    lRun.grid(row = 0, column = 4, pady = 2)
    eRun = tk.Entry(tabPlotting)
    eRun.insert(0, '0')
    eRun.grid(row = 1, column = 4, pady = 2)
    
    lIntersectIntegrate = tk.Label(tabPlotting, text = 'Intersection\nActive')
    lIntersectIntegrate.grid(row = 0, column = 5, pady = 2)
    bIntersectIntegrate = tk.Button(tabPlotting, text = 'Integrate', command = intersectIntegrate)
    bIntersectIntegrate.grid(row = 1, column = 5, pady = 2)
    
    lMelt = tk.Label(tabPlotting, text = 'Enter Melting\nPoint')
    lMelt.grid(row = 0, column = 6, pady = 2)
    eMelt = tk.Entry(tabPlotting)
    eMelt.grid(row = 1, column = 6, pady = 2)
    
    lAutoNucTime = tk.Label(tabPlotting, text = 'Auto-Get\nNuc Times')
    lAutoNucTime.grid(row = 0, column = 7, pady = 2)
    bAutoNucTime = tk.Button(tabPlotting, text = 'Generate', command = autoNucTime)
    bAutoNucTime.grid(row = 0, column = 7, pady = 2)
    
    tk.mainloop()

if __name__ == '__main__':
    main()