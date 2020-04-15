import numpy as np
from scipy.optimize import curve_fit
import json
import requests
import time
from sklearn.metrics import mean_squared_error


# 60000~2000000
parameter_K = None
# 0~1
parameter_r = None

def logistic_function(t,P0):
    exp_r = np.exp(parameter_r * t)
    return parameter_K *P0 *exp_r / (parameter_K + P0 *(exp_r - 1))

url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_foreign&callback=&_=%d' % int(time.time() * 1000)
response = requests.get(url)

data = response.json()['data']
print(data)

data_dict = json.loads(data)

day_list = []
y_data = []
x_data = np.arange(len(y_data))

# foreign_list = data_dict['globalDailyHistory']
# for item in foreign_list:
#     y_data.append(item['confirm'])



# 遍历K和r
K_range = np.arange(60000,2000000,1000)
r_range = np.arange(0,1,0.001)

# 表示正负无穷数
loss = float('inf')

optimal_K = None
optimal_r = None
optimal_P0 = None

i = 0

for K_ in K_range:
    for r_ in r_range:
        parameter_K = K_
        parameter_r = r_

        popt, pcov = curve_fit(logistic_function, x_data, y_data)

        # 从循环中找出最优的一次，让logistics_function最符合预测
        loss_ = mean_squared_error(y_data,logistic_function(x_data,popt))

        if loss_ < loss:
            loss = loss_
            optimal_K = K_
            optimal_r = r_
            optimal_P0 = popt

        i += 1

        # print('\r拟合进度：{0}{1}%'.format('0' * int(10 * i / len(K_range) / len(r_range)),
        #                                         int(100 * i / len(K_range) / len(r_range))),end='')

print('optimal_K:',optimal_K)
print('optimal_r:',optimal_r)
print('optimal_P0:',optimal_P0)

