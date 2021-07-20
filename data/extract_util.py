# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 16:42:12 2021

@author: 11911627 Tan Sixu
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal



def low_pass_filter(raw_data):
    '''
    

    Parameters
    ----------
    raw_data : ndarray
        raw data sampled

    Returns
    -------
    df_filter : ndarray
        after low pass filter

    '''
    raw_data=raw_data/1000+1
    df_raw = pd.Series({'Raw data':raw_data})
    df_filter = df_raw.rolling(11).mean()
    return df_filter.values


# def window_selection(window_size, overlap, data)
    
    
    
def valley_detection(data, threshold):
    valey_args=[]
    for i in range(1, len(data)):
        if data[i-1]-data[i] > threshold and data[i+1]-data[i] > threshold:
            valey_args.append(i)
    return np.array(valey_args)


aa = np.load('x_data.npy')/1000+1
df1=pd.Series(aa)
df2=df1.rolling(11).mean()
df2=df2.values
# df1.plot()
df3=scipy.signal.savgol_filter(df2,11,7)
plt.plot(df3)  
plt.plot(df2, 'b')
valey=valley_detection(df2, 0.008)
plt.scatter(valey, df2[valey], c='r')
plt.show()