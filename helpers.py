import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  
import io
import random
#from dtw import * #pip install dtw-python
from fastdtw import fastdtw # pip install fastdtw
from itertools import islice
import statistics
import math

import ipywidgets as widgets
from IPython.display import display,Javascript, Markdown, Latex,HTML



#  plot using matplotlib
def myplot(lst,xlabel="",ylabel="",title=""):
    plt.rcParams.update({'font.size': 14})
    plt.rcParams['axes.facecolor'] = '#eeeeee'
    plt.rcParams['figure.figsize'] = (20, 10)
    plt.grid(axis='y', color = '#cccccc', linestyle = '--', linewidth = 1)
    plt.grid(axis='x', color = '#eeeeee', linestyle = '--', linewidth = 1)
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.plot(lst,linewidth=2)
    
# downsample a list to a certain proportion
# proportion =1, 0.5, 0.25 ,etc
# if the proportion = 0.5, then we pick one sample among each two samples. So, the resulting list length will be half the original length
def downsample(values, proportion=1):
    return list(islice(values, 0, len(values), int(1/proportion)))

# remove leading and lagging values under certain upper threshold
#works with lists
def trim_list_under(lst,upper):
    first=0
    last=len(lst)-1
    for i in range(0,len(lst)):
        if lst[i] > upper:
            first=i
            break
    for i in range(len(lst)-1,-1,-1):
        if lst[i] > upper:
            last=i
            break
            
    return lst[first:last+1]  

# remove leading and lagging values under certain upper threshold
#works with dataframe
def trim_df_under(df,upper):
    first=0
    last=len(df)-1
    for i in range(0,len(df)):
        if df[f'{appliance}'].values[i] > upper:
            first=i
            break
    for i in range(len(df)-1,-1,-1):
        if df[f'{appliance}'].values[i]  > upper:
            last=i
            break
            
    return df.iloc[first:last+1,:]  


from collections import deque
from bisect import insort, bisect_left
from itertools import islice
def moving_median(seq, window_size):
    """Contributed by Peter Otten"""
    seq = iter(seq)
    d = deque()
    s = []
    result = []
    for item in islice(seq, window_size):
        d.append(item)
        insort(s, item)
        result.append(s[len(d)//2])
    m = window_size // 2
    for item in seq:
        old = d.popleft()
        d.append(item)
        del s[bisect_left(s, old)]
        insort(s, item)
        result.append(s[m])
    # at this point, the 'result' contains the smoothe values, but, the first elements with size 'window_size' are copied from the original list. Therefore, the smoothing is shifted and needs centering
    
    #centering the list
    result=result[window_size-1:len(result)]
    padd = window_size//2
    r1 = [result[0]]*(padd)
    r2=  result 
    r3 =[result[len(result)-1]]*(padd - 1)
    result = r1+r2+r3
    return result

# somple moving average using convolution
def moving_average(lst, window_size):
    return np.convolve(list, np.ones(window_size), 'valid') / window_size


import os, os.path
from os import listdir
#reads a list of csv files from a directory.
#each csv file contains a pandas dataframe that represents a SUP. The name of the file follows h1_wahser00.csv,..,h1_wahser32.csv
#SUP files are stored in order so that each cluster are adjacent.
#SUP files are stored in a directory named with the appliance name
def read_SUPs(house,appliance):
    path = f'house{house}/{appliance}'
    files=[f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))]
    num_files = len(files)

    SUPs=[]
    for i in range(0,num_files):
        try:
            SUPs.append(  pd.read_csv(f'house{house}/{appliance}/h{house}_{appliance}{i:02d}.csv'))
        except:
            pass
    return SUPs

# plots all SUPs
# together=True means all plots are in the same figure
def plot_SUPs(SUPs,together=True):
    for i in range(0,len(SUPs)):
        if together == False:
            plt.figure(i)
        plt.xlabel(f'SUP[{i:02d}]')
        myplot(SUPs[i])