# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 01:31:07 2020

@author: drewvigne

This code is meant to sweep Star-CCM+ Design Manager Log files for rich
data analysis and visualization.

It was specifically made to capture 2D Airfoil polars at multiple Reynolds
numbers and Angles of Attacks for use with Blade Element Momentum applications.
In this case, the airfoil in question was a cross-section of the HED Trispoke.

Note that this is dependent on steady state RANS solutions of 2500 iterations.
Best for use with Spyder.

"""

import pandas as pd
import matplotlib.pyplot as plt
import math as m

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# User input. Use data sweep ranges from Design Manager. AoA in degrees.

aoaStart = 0 
aoaEnd = 180
aoaStep = 3

reStart = 100000
reEnd = 500000 
reStep = 40000

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Other useful variables.

aoaNum = int((aoaEnd + aoaStep - aoaStart) / aoaStep)
reNum = int((reEnd + reStep - reStart) / reStep)
caseNum = int(reNum*aoaNum)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Sorts through log files, tabulates relevant data, and plots it.

def sortRaw(number):
    caseNumber = str(number)

    df = pd.read_csv("spokeAnalysisStudy3\Design_" + caseNumber + "\Design_"\
                     + caseNumber + ".log", delim_whitespace=True,\
                     skiprows=500, nrows=1500, error_bad_lines=False)
    
    
    df = df.apply (pd.to_numeric, errors='coerce')
    df = df.dropna()
    df = df.reset_index(drop=True)
    

    df.columns = ['Iter','Continuity','X-mom','Y-mom','Sa-Nut','Cd','Cl','AoA']
 
    
    avgCl = [df["Cl"].mean(),df["Cl"].mean()]
    avgCd = [df["Cd"].mean(),df["Cd"].mean()]
    xAxis = [df["Iter"].iloc[0], df["Iter"].iloc[-1]]

    
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))

    ax1.plot(xAxis, avgCd, 'r--')
    ax1.set_title("Drag Coefficient")
    df.plot(y='Cd', x='Iter', ax=ax1, color='black')

    ax2.plot(xAxis, avgCl, 'r--')
    ax2.set_title("Lift Coefficient")
    df.plot(y='Cl', x='Iter', ax=ax2, color='black')

    fig.suptitle('Spoke Analysis Case ' + caseNumber, fontsize=16) 
    
    favgCd = df["Cd"].mean()
    favgCl = df["Cl"].mean()
    AoA = 180 * df["AoA"].iloc[0] * (1/m.pi)

    return AoA, favgCd, favgCl

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Automatically adds Reynolds number column to dataframe.

reList = []

for re in range(reStart, reEnd+reStep, reStep):
    for i in range(0, aoaNum):
        reList.append(re)


newData = []

for j in range(1,caseNum+1):
    newData.append(sortRaw(j))
df = pd.DataFrame(newData, columns=["AoA", "Avg Cd", "Avg Cl"])

df['Re'] = pd.Series(reList, index=df.index)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Sort by each Re and plot the avg Cd anc Cl curves.

dfs = locals()

for re in range(reStart, reEnd+reStep, reStep):
    strRe = str(re)
    dfs["df{0}".format(re)] = df.loc[df['Re'] == re]
    
    
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))

    ax1.set_title("Avg Drag Coefficient vs. AoA")
    dfs["df{0}".format(re)].plot(y='Avg Cd', x='AoA', ax=ax1, color='red')

    ax2.set_title("Avg Lift Coefficient vs. AoA")
    dfs["df{0}".format(re)].plot(y='Avg Cl', x='AoA', ax=ax2, color='red')

    fig.suptitle('Reynolds Number ' + strRe, fontsize=16)













