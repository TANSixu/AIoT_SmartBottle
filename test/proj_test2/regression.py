# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 21:25:51 2021

@author: 11911627 Tan Sixu
"""

import pandas as pd
from sklearn.neural_network import  MLPRegressor
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import pickle
from sklearn.svm import SVR
from sklearn.ensemble import GradientBoostingRegressor
from untitled5 import*

file = 'new_data2.csv'

record = pd.read_csv(file)
raw = []
for i in range(len(record)):
    f = record.loc[i]
    raw.append(list(f))
    
np.random.shuffle(raw)


features=[]
labels = []
for r in raw:
    features.append(r[:-2])
    labels.append(r[-1])
        
features=np.abs(np.array(features))
labels=np.array(labels)
    
f_train, f_test, l_train, l_test = train_test_split(features, labels, test_size = 0.9
                                                    , random_state=None)


# ss_x,ss_y = StandardScaler(),StandardScaler()
# f_train = ss_x.fit_transform(f_train)
# f_test = ss_x.transform(f_test)
# l_train = ss_y.fit_transform(l_train.reshape([-1,1])).reshape(-1)
# l_test = ss_y.transform(l_test.reshape([-1,1])).reshape(-1)


# svm=SVR(kernel='linear', tol=1e-7, C=0.041)
# svm.fit(f_train, l_train)

with open('svmModel.pkl', 'rb') as file:
    svm = pickle.load(file)

spp=svm.predict(f_test)
# print(predict_amt(f_test[1], svm))
# spp=ss_y.inverse_transform(spp)
# l_test=ss_y.inverse_transform(l_test)

dd = np.mean((abs(spp - l_test)/l_test))

# print(dd)

print(dd)

for i in range(len(spp)):
    # print(f'real:{l_test[i]}, deviation: {ppp[i]-l_test[i]}')
    print(f'real:{l_test[i]}, prediction: {spp[i]}')
    
#%%



# model_Grad = GradientBoostingRegressor(n_estimators=1000, tol=1e-5)#这里使用100个决策树
# model_Grad.fit(f_train, l_train)

# gpp = model_Grad.predict(f_test)

# # gpp=ss_y.inverse_transform(gpp)
# # l_test=ss_y.inverse_transform(l_test)


# dd = np.mean((abs(gpp - l_test)/l_test))

# # print(dd)

# print(dd)

# for i in range(len(gpp)):
#     # print(f'real:{l_test[i]}, deviation: {ppp[i]-l_test[i]}')
#     print(f'real:{l_test[i]}, prediction: {gpp[i]}')


#%%
# # ANN
NNmodel = MLPRegressor([1000,600],learning_rate_init= 0.00001,activation='relu',\
      solver='adam', alpha=0.0001,max_iter=60000)  # 神经网络


# with open('model5.pkl', 'rb') as file:
#     NNmodel = pickle.load(file)

#Second 训练数据
print('start train!')
NNmodel.fit(f_train,l_train)

print('end train!')
#Third 检验训练集的准确性
ppp = NNmodel.predict(f_test)
# ppp = ss_yl.inverse_transform(ppp)
# l_test = ss_yl.inverse_transform(l_test)
dd = np.mean((abs(ppp - l_test)/l_test))

print(dd)
for i in range(len(ppp)):
    # print(f'real:{l_test[i]}, deviation: {ppp[i]-l_test[i]}')
    print(f'real:{l_test[i]}, prediction: {ppp[i]}')

#%%


svm=SVR(kernel='rbf',C=10,gamma=0.1,probability=True)
svm.fit(f_train, l_train)

spp=svm.predict(f_test)