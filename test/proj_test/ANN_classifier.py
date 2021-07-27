# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 16:27:48 2021

@author: 11911627 Tan Sixu
"""

import pandas as pd
from sklearn.neural_network import  MLPClassifier
import numpy as np
from sklearn.model_selection import train_test_split

record = pd.read_csv('data_set.csv')
raw = []
for i in range(len(record)):
    f = record.loc[i]
    raw.append(list(f[0:-1]))
    
np.random.shuffle(raw)


features=[]
label = []
for r in raw:
    features.append(r[:4])
    label.append(r[4])
    
f_train, f_test, l_train, l_test = train_test_split(features, label, test_size = 0.1, random_state=None)

NNmodel = MLPClassifier([100,60],learning_rate_init= 0.001,activation='tanh',\
     solver='adam', alpha=0.0001,max_iter=30000)  # 神经网络
#Second 训练数据
print('start train!')
NNmodel.fit(f_train,l_train)
print('end train!')
#Third 检验训练集的准确性
ppp = NNmodel.predict(f_test)
dd = np.sum(np.square(ppp - l_test))

print(dd)
