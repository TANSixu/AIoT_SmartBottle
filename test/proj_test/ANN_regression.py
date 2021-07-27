# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 16:46:46 2021

@author: 11911627 Tan Sixu
"""

import pandas as pd
from sklearn.neural_network import  MLPRegressor
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import pickle

file = 'test_set5.csv'

record = pd.read_csv(file)
raw = []
for i in range(len(record)):
    f = record.loc[i]
    raw.append(list(f))
    
np.random.shuffle(raw)


features=[]
labels = []
for r in raw:
    if(r[4]==1 and r[5]<60):
        features.append(r[:4])
        labels.append(r[5])
        
features=np.array(features)
labels=np.array(labels)
    
f_train, f_test, l_train, l_test = train_test_split(features, labels, test_size = 0.9
                                                    , random_state=None)


# ss_xt,ss_yt, ss_xl, ss_yl = StandardScaler(),StandardScaler(),StandardScaler(),StandardScaler()
# f_train = ss_xt.fit_transform(f_train)
# f_test = ss_xl.fit_transform(f_test)
# l_train = ss_yt.fit_transform(l_train.reshape([-1,1])).reshape(-1)
# l_test = ss_yl.fit_transform(l_test.reshape([-1,1])).reshape(-1)


# # ANN
# NNmodel = MLPRegressor([100,60],learning_rate_init= 0.000019,activation='relu',\
#       solver='adam', alpha=0.0001,max_iter=60000)  # 神经网络


with open('model5.pkl', 'rb') as file:
    NNmodel = pickle.load(file)

# #Second 训练数据
# print('start train!')
# NNmodel.fit(f_train,l_train)

# print('end train!')
#Third 检验训练集的准确性
ppp = NNmodel.predict(f_test)
# ppp = ss_yl.inverse_transform(ppp)
# l_test = ss_yl.inverse_transform(l_test)
dd = np.mean((abs(ppp - l_test)/l_test))


print(dd)
for i in range(len(ppp)):
    # print(f'real:{l_test[i]}, deviation: {ppp[i]-l_test[i]}')
    print(f'real:{l_test[i]}, prediction: {ppp[i]}')



#Random forest

# ss_x,ss_y = StandardScaler(),StandardScaler()
# f_train = ss_x.fit_transform(f_train)
# f_test = ss_x.transform(f_test)
# l_train = ss_y.fit_transform(l_train.reshape([-1,1])).reshape(-1)
# l_test = ss_y.transform(l_test.reshape([-1,1])).reshape(-1)

# rfr = RandomForestRegressor()
# rfr.fit(f_train,l_train)
# pp = rfr.predict(f_test)
# dd = np.mean((abs(pp - l_test)/l_test))

# print(dd)

