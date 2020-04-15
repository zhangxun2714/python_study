

import requests
import time
import json
import matplotlib.pyplot as plt


url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d' % int(time.time() * 1000)
response = requests.get(url)

#print(response.text)

response_json = response.json()
#print(response.json())

data = response_json['data']
#print(data)

data_dict = json.loads(data)
#print(data_dict)

china_list = data_dict['areaTree'][0]['children']
#print(china_list)


province_name = []
province_confirm = []
for province in china_list:
    province_name.append(province['name'])
    province_confirm.append(province['total']['confirm'])


plt.rcParams['font.sans-serif'] = 'SimHei'   # 使图形中的中文正常编码显示

#条形图
plt.bar(province_name,province_confirm)
plt.xticks(rotation=-60)
plt.xlabel('省份')
plt.ylabel('确诊人数')
plt.title('全国各省确诊人数')
plt.show()