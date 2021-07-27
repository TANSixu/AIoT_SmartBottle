# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 14:42:38 2021

@author: 11911627 Tan Sixu
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import polyfit, poly1d
import collections


def low_pass_filter(raw_data, rolling_size):
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
    raw_data=-raw_data/1000
    df_raw = pd.Series(raw_data)
    df_filter = df_raw.rolling(rolling_size).mean()
    return df_filter.values


# def window_selection(window_size, overlap, data)
    
    
    
    
def valley_detection(data, threshold, local_num, safe_limit):
    '''
    

    Parameters
    ----------
    data : ndarr
        input array
    threshold : int
        Deviation surpass the threshold, then detect as valley
    local_num : int
        Check the nearest {local_num} points as mean.
    safe_limit : int
        Once beyond the limit, exclude from valley

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    valey_args=[]
    data = -(data-1)
    for i in range(1, len(data)):
        if data[i] <= safe_limit and np.mean(data[max(i-local_num, 1):i])-data[i] > threshold and np.mean(data[min(i+1, len(data)-1):min(i+local_num, len(data)-1)])-data[i] > threshold:
            valey_args.append(i)
    return np.array(valey_args)


def threshold(data_x, data_y, data_z, valleys, x_thresh, y_thresh):
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
    
    #change to origin
    data=-(data_x-1)
    diff = [valleys[i]-valleys[i-1] for i in range(1, len(valleys))]
    diff = np.array(diff)
    index = np.argwhere(diff>x_thresh)
    index = index.reshape(len(index))
    
    for i in index:
        candicate = data[valleys[i]:valleys[i+1]+1]
        if max(candicate) > y_thresh:
            can_x = data_x[valleys[i]:valleys[i+1]+1]
            can_y = data_y[valleys[i]:valleys[i+1]+1]
            can_z = data_z[valleys[i]:valleys[i+1]+1]
            satisfy.append((can_x, can_y, can_z))
    
    return satisfy


def feature_extract(data_segment):
    
    x=[i for i in range(len(data_segment))]
    x1=np.linspace(0,len(data_segment)-1, 1000)
    poly = poly1d(polyfit(x, data_segment, 17))
    fit = poly(x1)
    
    slope = lambda x, f: (f[x+8]-f[x])/8
    epsilon = 0.01
    for v in range(np.argwhere(abs(fit-0.5)<epsilon)[0][0],np.argmax(fit), 1 ):
        if slope(v, fit)<slope(v-1, fit):
            sip_start=v
            break
    
    H = max(fit)-min(fit)
    duration = (len(data_segment)/1000)*(np.argmax(fit)-sip_start)
    avg = np.mean(fit)
    ratio = np.argmax(fit)/(1000-np.argmax(fit))
    return [[H, duration, avg, ratio]]


# For test only

def sip_bound(rolling_alpha, threshold):
    '''
    

    Parameters
    ----------
    rolling_alpha : ndarr
        The discrete value of alpha, which indicates the yz axis rotation
    threshold : int
        The acceptable bound of fluctuation

    Returns (tuple)
    -------
    left : int
        The index of found left bound.
    right : int
        The index of found right bound.

    '''
    
    aa = rolling_alpha
    mid = len(aa)//2
    left = mid-1
    right = mid+1
    end1=False
    end2=False
    while not (end1 and end2):
        if left-1>=0 and abs(np.mean(aa[left:right])-aa[left-1])<threshold:
            left-=1
        else:
            end1=True
        
        if right+1<len(aa) and abs(np.mean(aa[left:right])-aa[right+1])<threshold:
            right+=1
        else:
            end2=True
            
    return left, right

def numerical_derivative(arr):
    '''
    This function calculate the approximation of numerical derivative. 
    By default step length of 2 is set.
    
    Parameters
    ----------
    arr : ndarr
        The input discrete array.

    Returns
    -------
    TYPE ndarr
        The derivative of each point within arr.

    '''
    
    derivative = []
    derivative.append(arr[1]-arr[0])
    for i in range(1, len(arr)-1):
        derivative.append((arr[i+1]-arr[i-1])/2)
        
    derivative.append(arr[-1]-arr[-2])
    return np.array(derivative)



def feature_engineering(sip_theta):
    '''
    Extract the total 33 features of the data, referring to the article.

    Parameters
    ----------
    sip_theta : ndarr
        The theta values bounded by sip event.

    Returns ordered dict
    -------
    feature: dict contains all 33 features.

    '''
    
    
    feature=collections.OrderedDict()
    
#1
    theta_max = np.max(sip_theta)
    feature['theta_max']=theta_max
    
#2    
    duration = len(sip_theta)
    feature['duration']=duration
    
#3-11 
    T = [i*10 for i in range(2, 10)]
    A_theta=[]
    A_theta.append(np.count_nonzero(sip_theta<T[0]))
    
    for i in range(1, len(T)):
        A_theta.append(np.count_nonzero((sip_theta>=T[i-1]) & (sip_theta<T[i])))
    
    A_theta.append(np.count_nonzero(sip_theta>=T[-1]))
    # feature['A_theta']=A_theta
    
# 12-20
    P = [i/10 for i in range(2,10)]
    AR = []
    normal = sip_theta/theta_max
    AR.append(np.count_nonzero(normal<P[0]))
    
    for i in range(1, len(P)):
        AR.append(np.count_nonzero((normal>=P[i-1]) & (normal<P[i])))
    
    AR.append(np.count_nonzero(normal>=P[-1]))
    # feature['AR']=AR
    
#21
    ratio_Max_D = theta_max/duration
    feature['ratio_Max_D']=ratio_Max_D
    
#22
    avg_theta = np.mean(sip_theta)
    feature['avg_theta']=avg_theta
    
#23
    ratio_inc_dec = np.argmax(sip_theta)/(duration - np.argmax(sip_theta))
    feature['ratio_inc_dec']=ratio_inc_dec
    
#24-25
    Riemann = lambda arr, a, b: np.sum((arr[a:b-1]+arr[a+1:b])/2)
    
    s_entire = Riemann(sip_theta, 0, duration)
    s_incline = Riemann(sip_theta, 0, np.argmax(sip_theta)+1)
    feature['s_entire']=s_entire
    feature['s_incline']=s_incline
    
#26
    RE = (theta_max-sip_theta[0])/(np.argmax(sip_theta))
    feature['RE']=RE
    
#27
    FE = (sip_theta[-1]-theta_max)/(duration-np.argmax(sip_theta))
    feature['FE']=FE

#28-33
    deri_inc = numerical_derivative(sip_theta[:np.argmax(sip_theta)+1])
    deri_dec = numerical_derivative(sip_theta[np.argmax(sip_theta):duration])
    
    
    # 28-29
    max_inc = np.max(deri_inc)
    max_dec = np.min(deri_dec)      #I guess that here should be min, since it's negative
    
    feature['max_inc']=max_inc
    feature['max_dec'] = max_dec
    
    #30-31
    avg_inc = np.mean(deri_inc)
    avg_dec = np.mean(deri_dec)
    
    feature['avg_inc']=avg_inc
    feature['avg_dec']=avg_dec
    
    #32-33
    std_inc = np.std(deri_inc)
    std_dec = np.std(deri_dec)
    
    feature['std_inc']=std_inc
    feature['std_dec']=std_dec
    
    feature['A_theta']=A_theta
    feature['AR']=AR
    
    return feature


def predict_amt(flat_feature, ML_model):
    '''
    This function predict the dring amount using given ML model.

    Parameters
    ----------
    flat_feature : List
        List of flattened features.
    ML_model : 
        Model loads from pickle, pre-trained.

    Returns
    -------
    amt : double
        The predicted drinking amount

    '''
    
    flat_feature = np.abs(np.array(flat_feature)).reshape(1,-1)
    amt = ML_model.predict(flat_feature)
    return amt[0]
    
    
    

    
    
    
    
    






