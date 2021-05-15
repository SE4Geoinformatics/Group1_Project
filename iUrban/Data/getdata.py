# -*- coding: utf-8 -*-
"""
Created on Sat 15/05/2021

@author: Guangyu Ding
"""

import requests
import json
import pandas as pd
import re

#get url and data
url='https://five.epicollect.net/api/export/entries/san-silvestre-geography-ia-2020?per_page=451'
response = requests.get(url)
raw_data = response.text
data = json.loads(raw_data)
data = data['data']['entries']

colum_name = []
for col_name in data[0].keys():
    colum_name.append(col_name)
ind=list(range(len(data)))
df=pd.DataFrame(data, index=ind, columns=colum_name)

#correct the stupid name
for t in range(0,451):
    if re.match('Constanza Guerinoni.*', df.iloc[t,4])!=None:
        df['1_Name'][t]='Constanza Guerinoni'

#get the correct positions        
latitude=[]
longitude=[]
for i in range(0,451):
    meta=data[i]
    latitude.append(meta['2_Location']['latitude'])
    longitude.append(meta['2_Location']['longitude'])
    
#make the attributes correct
author=[0]*451
df=df.drop(['ec5_uuid'] , axis = 1)
df=df.drop(['uploaded_at'] , axis = 1)
df=df.drop(['title'] , axis = 1)
df=df.drop(['2_Location'] , axis = 1)
df.insert(0,'author_id',author)
df.insert(5,'latitude',latitude)
df.insert(6,'longitude',longitude)
df['author_id']=author
df.rename(columns = {'created_at':'created_date','1_Name':'name',
                     '3_Date':'date','4_Time':'time',
                     '5_Average_noise_leve':'average_noise_level',
                     '6_Average_light_inte':'average_light_intensity',
                     '7_Wind_direction':'wind_direction',
                     '8_Wind_speed_Beaufor':'wind_speed',
                     '9_Cloud_cover':'cloud_cover',
                     '10_Cloud_type':'cloud_type',
                     '11_Photo_of_cloud_co':'cloud_photo_id',
                     '12_Visibility':'visibility',
                     '13_Traffic_count':'traffic_count',
                     '14_Temperature':'temperature',
                     '15_Humidity':'humidity',
                     '16_Photo_of_you_coll':'collecting_photo_id',
                     '17_Make_a_note_of_an':'note_of_anomaly',
                     '18_Air_pollution_num':'air_pollution',
                     },inplace = True)

#title=['data_id', 'author_id', 'created_date', 'name',
#       'date', 'time', 'latitude', 'longitude', 'average_noise_level',
#       'average_light_intensity', 'wind_direction', 'wind_speed',
#       'cloud_cover', 'cloud_type', 'cloud_photo_id', 'visibility',
#       'traffic_count', 'temperature', 'humidity', 'collecting_photo_id',
#       'note_of_anomaly', 'air_pollution']
df.to_csv('E:/geoinfosys/se/data/testdata2.csv')