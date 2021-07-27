# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 17:00:44 2021

@author: 11911627 Tan Sixu
"""
from untitled5 import*

aa = np.load('./data/new_new_dataset4.npy')
x= aa[0]
y=aa[1]
z=aa[2]

tx=low_pass_filter(x, 6)
ty=low_pass_filter(y, 6)
tz=low_pass_filter(z, 6)


valley = valley_detection(tx, 0.001, 2, 0.2)
check = threshold(tx, ty, tz, valley, 15, 0.4)

# plt.plot(-tx+1)
# plt.axhline(y=0.4)
# plt.show()

now_exam=17


cx= check[now_exam][0]
cy= check[now_exam][1]
cz= check[now_exam][2]

theta = np.arctan(np.square(cy**2+cz**2)/cx)
alpha = np.arctan(cz/cy)
theta = (np.rad2deg(theta)+180)%180
alpha = np.rad2deg(alpha)


safe=sip_bound(alpha, 7)

plt.figure(figsize=(6, 18))
plt.subplot(3, 1, 1)



plt.plot(cx, label='x')
# plt.plot(theta, label='theta')
# plt.plot(alpha, label = 'alpha')
plt.plot(cy, label='y')
plt.plot(cz, label='z')
plt.axhline(y=0)

plt.axvline(x=safe[0], ls='--', zorder=-1, color='grey')
plt.axvline(x=safe[-1], ls='--', zorder=-1, color='grey')

plt.legend()

plt.subplot(3, 1, 2)
plt.plot(theta, label='theta')
plt.axvline(x=safe[0], ls='--', zorder=-1, color='grey')
plt.axvline(x=safe[-1], ls='--', zorder=-1, color='grey')

plt.legend()

plt.subplot(3, 1, 3)
plt.plot(alpha, label = 'alpha')

plt.legend()

plt.tight_layout()
plt.show()

# feature = feature_engineering(theta[safe[0]:safe[1]+1])
# for k, v in feature.items():
#     print(f'{k}: {v}')


# record = pd.DataFrame(columns=(['theta_max', 'duration', 'ratio_md','avg_theta','ratio_inc_dec','s_entire','s_incline','RE','FE' 
# ,'max_inc','max_dec', 'avg_inc', 'avg_dec', 'std_inc', 'std_dec',
# 'A1', 'A2', 'A3', 'A4', 'A5','A6', 'A7', 'A8','A9', 'AR1','AR2','AR3','AR4','AR5','AR6','AR7','AR8','AR9','label', 'amount']))

# record.to_csv('new_data2.csv', index=0)

#%%
def transform_data(feature):
    '''
    This function unpack the feature data into falt 33 items. Specifically, unpack the two list in it.

    Parameters
    ----------
    feature : ordered dict
        The feature returned from feature engineering.

    Returns
    -------
    in_feature :list
        Flattened 33 features.

    '''
    
    f_list = list(feature.values())
    in_feature = f_list[:-2]
    for a in f_list[-2]:
        in_feature.append(a)
    for a in f_list[-1]:
        in_feature.append(a)
    return in_feature

def record_data(all_segments):
    '''
    This function helps to record drinking amount.

    Parameters
    ----------
    all_segments : list
        List of all valid theta data segment.

    Returns
    -------
    None.

    '''
    
    record = pd.read_csv('new_data2.csv')
    for i in range(len(all_segments)):
        c = all_segments[i]
        cx= c[0]
        cy= c[1]
        cz= c[2]
        
        theta = np.arctan(np.square(cy**2+cz**2)/cx)
        alpha = np.arctan(cz/cy)
        theta = (np.rad2deg(theta)+180)%180
        alpha = np.rad2deg(alpha)
        
        safe=sip_bound(alpha, 7)
        raw_feature = feature_engineering(theta[safe[0]:safe[1]+1])
        t_feature = transform_data(raw_feature)
        
        print('-'*10)
        print(f'Now checking mountain {i}')
        # label = int(input('label as: '))
        t_feature.append(1)
        # if label == 0:
        #     f[0].append(-1)
    
        water = float(input('How much you drank: '))
        t_feature.append(water)
        record.loc[len(record)] = t_feature
    
    record.to_csv('new_data2.csv', index=0)
    print('done.')
    
record_data(check)
    

    
    
    