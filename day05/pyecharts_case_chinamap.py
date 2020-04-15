from pyecharts.charts import Map
from pyecharts import options as opts
import json
import requests
import time

url = 'http://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d' %int(time.time() * 1000)

data = json.loads(requests.get(url=url).json()['data'])

provience_data = data['areaTree'][0]['children']

provience_confirm_data = {}
for provience_data in provience_data:
    provience_confirm_data[provience_data['name']] = provience_data['total']['confirm']

virus_map = Map()
virus_map.add('中国疫情地图', data_pair=provience_confirm_data.items())
virus_map.set_global_opts(
    visualmap_opts=
    opts.VisualMapOpts(split_number=6,
                       is_pieces=True,
                       pieces=[{'min':1,'max':9,'label':'1-9人','color':'#ffefd7'},
                               {'min':10,'max':99,'label':'10-99人','color':'#ffd2a0'},
                               {'min':100,'max':499,'label':'100-499人','color':'#fe8664'},
                               {'min':500,'max':999,'label':'500-999人','color':'#e64b47'},
                               {'min':1000,'max':9999,'label':'1000-9999人','color':'#c91014'},
                               {'min':10000,'label':'10000人及以上','color':'#9c0aOd'}]),
    title_opts=opts.TitleOpts(title='中国确诊病例地图'))
virus_map.render()