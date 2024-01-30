# DSC Analyze

### Purpose:
The DSC outputs data into a csv format that is difficult to use out of the box. In addition, the large quantity of data can be too much for excel to manage. This program seeks to automatically reformat the data into a more workable state and to help extract useful data points.

### Running instructions:
This program requires the packages pandas, numpy, matplotlib, and scipy to be downloaded into your python environment. To run the program, open a python terminal that has the required modules installed and run the following

`cd "filepath"`

where filepath can be found by right clicking or shift + right clicking the folder "DSC Analyze" and selecting "copy filepath". Next run 

`python DSCGUI.py`

and the window will open. Input the filepath of the csv you would like to analyze and click submit. If no error window appears, continue on to the data plotting section.

Enter the run number you would like to view, the default is 0 which plots all runs.

When performing an intersection or integration calculation, select points that move forward in time. This may be easier to perform in the time plot if the forward in time direction is not known.

To plot new data, move back to the settings tab and press the restart button.
