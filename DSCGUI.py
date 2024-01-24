# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 11:13:13 2023

@author: tyler
"""

import sys
import os
script_directory = os.path.realpath(os.path.dirname(__file__))
sys.path.append(script_directory)
import DSCDataClass as DC
import tkinter as TK
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.pyplot import close

def submitPath():
    global data
    
    try:
        path = ePath.get()
        
        if path[0] == r'"':
            path = path[1:]
        if path[-1] == r'"':
            path = path[:-1]

        runs = eRuns.get()
        steps = eSteps.get()
        data = DC.DSCData(path, int(runs), int(steps))
        
    except:
        messagebox.showinfo("Error", "Error in path, runs, or steps entry.")

def submitPlot():
    global data
    run = eRunSelect.get()
    try:
        data.plot(int(run), scatterBool)
    except Exception as error:
        messagebox.showinfo("Error", error)
        
    canvas = FigureCanvasTkAgg(data.fig, master = master)
    
    canvas.draw()
    
    canvas.get_tk_widget().grid(row = 1, column = 2, rowspan = 20)
    
    
    
    toolbar_frame = TK.Frame(master = master)
    toolbar_frame.grid(row = 21, column = 2)
    
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
    toolbar.update()

    # except Exception as error:
    #     messagebox.showinfo("Error", error)
    
def checked():
    global scatterBool
    if scatterBool == False:
        scatterBool = True
    else:
        scatterBool =False

def IntegrateChange():
    global IntegrateBool
    if IntegrateBool == False:
        data.pickerType = "Integrate"
    else:
        data.pickerType = "Point"

def on_closing():
    global data
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        master.destroy()
        close(data.fig)

def getTime():
    global data
    run = int(eRuns.get())
    
    lTime.config(text=[str(data.NucTime(x)) + '\n' for x in range(1, run+1)])

data = None
scatterBool = False
IntegrateBool = False

master = TK.Tk()
master.title("DSC Analyze")

lPath = TK.Label(master, text = 'File Path:')
lPath.grid(row = 0, column = 0, sticky = TK.W, pady = 2)
ePath = TK.Entry(master)
ePath.grid(row = 0, column = 1, columnspan = 3, stick = TK.W+TK.E, pady = 2)

lRuns = TK.Label(master, text = 'Runs:')
lRuns.grid(row = 1, column = 0, sticky = TK.W, pady = 2)
eRuns = TK.Entry(master)
eRuns.grid(row = 1, column = 1, pady = 2)

lSteps = TK.Label(master, text = 'Steps:')
lSteps.grid(row = 2, column = 0, sticky = TK.W, pady = 2)
eSteps = TK.Entry(master)
eSteps.grid(row = 2, column = 1, pady = 2)

bSubmit = TK.Button(master, text = 'Submit File Path', command = submitPath)
bSubmit.grid(row = 3, column = 0, columnspan = 2, pady = 2)

lRunSelect = TK.Label(master, text = 'Input run to plot, \nuse 0 to plot all runs')
lRunSelect.grid(row = 4, column = 0, sticky = TK.W, pady = 2)
eRunSelect = TK.Entry(master)
eRunSelect.grid(row = 4, column = 1, pady = 2)

lScatter = TK.Label(master, text='Make scatter plot?')
lScatter.grid(row = 5, column = 0, sticky = TK.W, pady = 2)
chScatter = TK.Checkbutton(master, command = checked)
chScatter.grid(row = 5, column = 1, pady = 2)

bPlot = TK.Button(master, text = 'Plot', command = submitPlot)
bPlot.grid(row = 6, column = 0, columnspan = 2, pady = 2)

bTime = TK.Button(master, text = 'Get Nucleation Time', command = getTime)
bTime.grid(row = 7, column = 0, pady = 2)
lTime = TK.Label(master, text='')
lTime.grid(row = 7, column = 1, pady = 2)

lRampRate = TK.Label(master, text = 'Ramp Rate:')
lRampRate.grid(row = 8, column = 0, sticky = TK.W, pady = 2)
eRampRate = TK.Entry(master)
eRampRate.grid(row = 8, column = 1, sticky = TK.W, pady = 2)

lIntegrate = TK.Label(master, text = "Integrate?")
lIntegrate.grid(row = 9, column = 0, sticky = TK.W, pady = 2)
chIntegrate = TK.Checkbutton(master, command = IntegrateChange)
chIntegrate.grid(row = 9, column = 1, sticky = TK.W, pady = 2)


TK.mainloop()

