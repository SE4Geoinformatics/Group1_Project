# -*- coding: utf-8 -*-
"""
Created on Sat 28/05/2021

@author: Group 1
"""

import os
import folium
from folium.plugins import HeatMap
import branca
import numpy as np
import pandas as pd
import geopandas as gp
from getdata import df
from folium.plugins import MarkerCluster
from datetime import datetime
import geopy
from geopy.geocoders import Nominatim

##pdreader = pd.read_csv('E:\\geoinfosys\\se\\data\\testdata2.csv', 'r', encoding="utf-8")


##print(pdreader)
originX=df.longitude[0]
originY=df.latitude[0]
X=df.longitude
Y=df.latitude
humidity=df.humidity
data=df[["latitude", "longitude", "humidity"]]


def city_map():
    city_map=folium.Map(location=[originY, originX], zoom_start=10, disable_3d = True)
    city_map.add_child(folium.LatLngPopup())
    city_map.save("E:\\geoinfosys\\se\\data\\mymap.html")
    return city_map
city_map()

def marker():
    markmap=city_map()
    colorlist = ['#ffffff','#b6f6ff','#6eedfe','#25e4ff','#00e6f1','#19ffbe','#46fe9c',
                 '#f6fa0f','#ffde00','#fbae00','#ff7f00','#ff5300','#fe2200','#ef0602','#c20000','#950101','#640002']
    colorbar = branca.colormap.StepColormap(colorlist,vmin = df.humidity.min(),vmax = df.humidity.max(), caption= 'humidity')
    for i in range(len(X)):
        folium.Circle(
                location=[Y[i],X[i]],
                radius=2,
                popup=df.humidity[i],
                color=colorbar(df.humidity[i]),
                fill=True,
                fill_opacity=0.5
                ).add_to(markmap)
    markmap.add_child(folium.LatLngPopup())
    markmap.add_child(colorbar)
    markmap.save("E:\\geoinfosys\\se\\data\\markmap.html")
marker()

def heatmap():
    heatmap=city_map()
    HeatMap(data).add_to(heatmap)
    heatmap.add_child(folium.LatLngPopup())
    heatmap.save('E:\\geoinfosys\\se\\data\\heatmap.html')
heatmap()

def clustered():
    clustermap=city_map()
    marker_cluster = MarkerCluster().add_to(clustermap)
    for i in range(len(X)):
        folium.Marker(
                location=[Y[i], X[i]],
                icon=None,
                popup=df.humidity[i],
                ).add_to(marker_cluster)
    clustermap.add_child(marker_cluster)
    clustermap.add_child(folium.LatLngPopup())
    clustermap.save("E:\\geoinfosys\\se\\data\\clustermap.html")
clustered()


def trade():
    linedata=df.loc[df['name']=='Constanza Guerinoni']
    linedata=linedata[["date","time","latitude","longitude"]]
    linedata['exact_time']=linedata.apply(lambda x:x['date']+" "+x['time'],axis=1)
#    date_time=[]
#    for i in range(len(linedata)):
#        date_time.append([linedata.iloc[i,0]+' '+linedata.iloc[i,1], linedata.iloc[i,2], linedata.iloc[i,3]])
    linedata=linedata.drop(['date'] , axis = 1)
    linedata=linedata.drop(['time'] , axis = 1)

    linedata=np.array(linedata)
    linedata=linedata.tolist()
    loc=[]
    listdata=sorted(linedata,key=lambda t:datetime.strptime(t[2], '%d/%m/%Y %H:%M:%S'))
    for i in range(len(linedata)):
        loc.append([listdata[i][0],listdata[i][1]])
    trademap=city_map()
    folium.PolyLine(
        loc,
        weight=4,
        color='red',
        opacity=0.8,
    ).add_to(trademap)


    folium.Marker(loc[0], popup='<b>Starting Point</b>').add_to(trademap)
    folium.Marker(loc[-1], popup='<b>End Point</b>').add_to(trademap)
    trademap.add_child(folium.LatLngPopup())
    trademap.save("E:\\geoinfosys\\se\\data\\trademap.html")
trade()

def polygon():
    poly_map = gp.GeoDataFrame.from_file("E:\geoinfosys\gadm36_PER_shp\selected.shp", encoding = 'utf-8')
    Poly_map = city_map()
    Poly_map.choropleth(
            geo_data=poly_map,
            key_on= 'feature.properties.NAME_1',
            fill_color='Red',
            fill_opacity=0.05,
            line_opacity=0.2)
    colorlist = ['#ffffff','#b6f6ff','#6eedfe','#25e4ff','#00e6f1','#19ffbe','#46fe9c',
                 '#f6fa0f','#ffde00','#fbae00','#ff7f00','#ff5300','#fe2200','#ef0602','#c20000','#950101','#640002']
    colorbar = branca.colormap.StepColormap(colorlist,vmin = df.humidity.min(),vmax = df.humidity.max(), caption= 'humidity')
    for i in range(len(X)):
        folium.Circle(
                location=[Y[i],X[i]],
                radius=2,
                popup=df.humidity[i],
                color=colorbar(df.humidity[i]),
                fill=True,
                fill_opacity=0.5
                ).add_to(Poly_map)
    position=gp.tools.geocode('Larco Museum', 'Nominatim' , user_agent='myuseragent')
    buffer=position.to_crs(epsg=7855).buffer(3000).to_crs(epsg=4326)
    folium.GeoJson(buffer).add_to(Poly_map)
    folium.GeoJson(position, tooltip=folium.GeoJsonTooltip(['address'])).add_to(Poly_map)
    Poly_map.add_child(folium.LatLngPopup())
    Poly_map.add_child(colorbar)
    Poly_map.save("poly_map.html")
polygon()

# def convert_toGJ():

