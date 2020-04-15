import matplotlib.pyplot as plt
import requests
import time
import json
from datetime import datetime

#中文
plt.rcParams['font.sans-serif'] = ['SimHei']


url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_other&callback=&_=%d' % int(time.time() * 1000)
response = requests.get(url)

print(response.text)


data = response.json()['data']
print(data)

data_dict = json.loads(response.json()['data'])
print(data_dict)

day_list = []
confirm_list = []
heal_list = []
dead_list = []

china_day_list = data_dict['chinaDayList']
for item in china_day_list:

    #04.03字符串转换 2020-04-03 的datatime对象
    month,day = item['date'].split('.')

    date = '2020-%s-%s' % (month,day)

    #strptime：把字符串转换成datatime
    date_format = datetime.strptime(date, '%Y-%m-%d')

    day_list.append(date_format)
    confirm_list.append(item['confirm'])
    heal_list.append(item['heal'])
    dead_list.append(item['dead'])

plt.plot(day_list,confirm_list,color='r',label='确诊')
plt.plot(day_list,heal_list,color='g',label='治愈')
plt.plot(day_list,dead_list,color='grey',label='死亡')

#显示图例 指定位置 防止被覆盖
plt.legend(loc='upper left')

#网格
plt.grid(linestyle=':')

plt.xlabel('日期')
plt.ylabel('人数')
plt.title('nCov-19国内疫情发展曲线')

plt.show()