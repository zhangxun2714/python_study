import numpy as np
from scipy.optimize import curve_fit
import json
import requests
import time
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import datetime as dt

url = 'https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=%E7%BE%8E%E5%9B%BD&'
response = requests.get(url)

usa_day_list = response.json()['data']
x_data_date = []
y_data = []
for item in usa_day_list:
    y_data.append(item['confirm'])
    x_data_date.append(item['date'])



parameter_K = None
parameter_r = None

def logistic_function(t,P0):
    exp_r = np.exp(parameter_r * t)
    return parameter_K * P0 *exp_r / (parameter_K + P0 *(exp_r -1))

x_data = np.arange(0, len(y_data))
print('x_data: ', x_data)
print('y_data: ', y_data)

x_data = np.arange(0,len(y_data))
print('x_data:',x_data)
print('y_data:',y_data)

# 遍历K和r
K_range = np.arange(460000,5000000,1000)
r_range = np.arange(0,1,0.01)

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

        popt, pcov = curve_fit(logistic_function,x_data,y_data)

        # 从循环中找出最优的一次，让logistics_function最符合预测
        loss_ = mean_squared_error(y_data,logistic_function(x_data,popt))

        if loss_ < loss :
            loss = loss_
            optimal_K = K_
            optimal_r = r_
            optimal_P0 = popt

        i += 1

        print('\r拟合进度：{0}{1}%'.format('▉' * int(10 * i / len(K_range) / len(r_range)),
                                      int(100 * i / len(K_range) / len(r_range))), end='')

print('\noptimal_K: ', optimal_K)
print('optimal_r: ', optimal_r)
print('optimal_P0: ', optimal_P0)

parameter_K = optimal_K
parameter_r = optimal_r

x_data_predict = np.arange(0, 100)
y_data_predict = logistic_function(x_data_predict, optimal_P0)
y_data_predict = y_data_predict.astype('int64')
print('y_data_predict: ', y_data_predict)

month, day = usa_day_list[0]['date'].split('.')
# 字符串转换为datetime
first_date = dt.datetime.strptime('2020-' + month + '-' + day, '%Y-%m-%d')
x_data_predict_date = [(first_date + (dt.timedelta(days=i))).strftime("%m.%d")
for i in range(100)]


# 中文乱码
plt.rcParams['font.sans-serif'] = ['SimHei']

plt.figure(figsize=(18, 6), dpi=300)

# 预测曲线图
plt.plot(x_data_predict_date, y_data_predict, linewidth='1.5', color='red',label='预测确诊')
# 实际点状图
plt.scatter(x_data_date, y_data, s=35, color='dimgrey', label='实际确诊')

plt.legend(loc='upper left')

plt.xticks(rotation=60)

plt.grid()

plt.ylabel('确诊人数')

plt.savefig('usa_predict.png', dpi=300)

plt.show()
