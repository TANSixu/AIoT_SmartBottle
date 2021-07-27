# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 16:42:12 2021

@author: 11911627 Tan Sixu
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import polyfit, poly1d


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
    raw_data=raw_data/1000+1
    df_raw = pd.Series({'Raw data':raw_data})
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
    for i in range(1, len(data)):
        if data[i] <= safe_limit and np.mean(data[max(i-local_num, 1):i])-data[i] > threshold and np.mean(data[min(i+1, len(data)-1):min(i+local_num, len(data)-1)])-data[i] > threshold:
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

aa = np.load('drinkornot_set11.npy')/1000+1
df1=pd.Series(aa)
df2=df1.rolling(11).mean()
df2=df2.values



valey=valley_detection(df2, 0.0008, 2, 0.2)
# plt.scatter(valey, df2[valey], c='r')
# plt.plot(df2)

check = threshold(df2, valey, 15, 0.5)



slope = lambda x, f: (f[x+10]-f[x])/10


# plt.axhline(y=0.5, color='g')

# now_exam=12

# x=[i for i in range(len(check[now_exam]))]
# x1=np.linspace(0,len(check[now_exam])-1, 1000)

# plt.plot(x,check[now_exam], 'r')

# epsilon = 0.01

# poly = poly1d(polyfit(x, check[now_exam], 17))
# y=poly(x1)

# # for v in range(np.argwhere(abs(y-0.5)<epsilon)[0][0],np.argmax(y), 1 ):
# #     if slope(v, y)<slope(v-1, y):
# #         sip=v
# #         break
        
# plt.axvline(x=x1[v])

# plt.plot(x1,y, 'g')



# plt.show()

record = pd.DataFrame(columns=(['H', 'duration', 'avg', 'ratio', 'label', 'amount']))
# record.to_csv('data_set.csv')

# file_name = 'data_set_fit.csv'

# record = pd.read_csv(file_name)
for i in range(len(check)):
    c = check[i]
    print('-'*10)
    print(f'Now checking mountain {i}')
    
    f = feature_extract(c)
    # label = int(input('label as: '))
    f[0].append(1)
    # if label == 0:
    #     f[0].append(-1)

    water = float(input('How much you drank: '))
    f[0].append(water)
    record.loc[len(record)] = f[0]
    
print('done.')
record.to_csv('test_set5.csv', index=0)





# record = pd.read_csv('data_set.csv')
# feature=[]
# label = []
# for i in range(len(record)):
#     f = record.loc[i]
#     feature.append(list(f[0:-2]))
#     label.append(f[-2])




