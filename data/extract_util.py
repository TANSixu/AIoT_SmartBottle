# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 16:42:12 2021

@author: 11911627 Tan Sixu
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


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
    
    
    
    
def valley_detection(data, threshold, local_num):
    '''
    

    Parameters
    ----------
    data : ndarr
        input array
    threshold : int
        Deviation surpass the threshold, then detect as valley
    local_num : int
        Check the nearest {local_num} points as mean.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    valey_args=[]
    for i in range(1, len(data)):
        if mean(data[max(i-local_num, 1):i])-data[i] > threshold and mean(data[min(i+1, len(data)-1):min(i+local_num, len(data)-1)])-data[i] > threshold:
            valey_args.append(i)
    return np.array(valey_args)


def threshold(data, valleys, x_thresh, y_thresh):
    '''
    

    Parameters
    ----------
    data : ndarr
        The signal data.
    valleys : ndarr
        The coordinates of all valley data.
    x_thresh : int
        Threshold of time.
    y_thresh : int
        Threshold of amptitude

    Returns
    -------
    list
        list of All satisified data segments.

    '''
    
    satisfy=[]
    
    diff = [valleys[i]-valleys[i-1] for i in range(1, len(valleys))]
    diff = np.array(diff)
    index = np.argwhere(diff>x_thresh)
    index = index.reshape(len(index))
    
    for i in index:
        candicate = data[valleys[i]:valleys[i+1]+1]
        if max(candicate) > y_thresh:
            satisfy.append(candicate)
    
    return satisfy


def feature_extract(data_segment):
    H = max(data_segment)-min(data_segment)
    duration = len(data_segment)
    avg = mean(data_segment)
    ratio = np.argmax(data_segment)/(duration-np.argmax(data_segment))
    return H, duration, avg, ratio


# For test only
# =============================================================================
# aa = -np.load('x_data2.npy')/1000+1
# df1=pd.Series(aa)
# df2=df1.rolling(6).mean()
# df2=df2.values
# # df1.plot()
# # df3=scipy.signal.savgol_filter(df2,11,7)
# # plt.plot(df3)  
# plt.plot(df2, 'b')
# valey=valley_detection(df2, 0.008, 2)
# plt.scatter(valey, df2[valey], c='r')
# check = threshold(df2, valey, 15, 1.0)
# # plt.plot(check[1])
# print(feature_extract(check[2]))
# plt.show()
# =============================================================================

