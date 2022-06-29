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
from psycopg2 import connect
from folium.plugins import MarkerCluster
from datetime import datetime
import geopy

# connect to database and catch data
conn = connect(host='localhost', port='5432', dbname='iUrbanDB',
               user='postgres', password='postgresql')
sql_command = "select * from TData"
try:
    df = pd.read_sql(sql_command, conn)
except:
    print("load data from postgres failure !")
    exit()

# set some static values
colorlist = ['#ffffff', '#b6f6ff', '#6eedfe', '#25e4ff', '#00e6f1', '#19ffbe', '#46fe9c',
             '#f6fa0f', '#ffde00', '#fbae00', '#ff7f00', '#ff5300', '#fe2200', '#ef0602', '#c20000', '#950101',
             '#640002']

ppup = []
for hud, vis, light in zip(
    list(df.humidity), list(df.visibility), list(df.average_light_intensity)
):
    strlist = 'Humidity:' + str(hud), 'Visibility:' + \
        str(vis), 'Light Intensity:' + str(light)
    ppup.append(strlist)
df.insert(df.shape[1]-1, 'pp', ppup)

originX = df.longitude[0]
originY = df.latitude[0]
X = df.longitude
Y = df.latitude
humidity = df.humidity
data = df[["latitude", "longitude", "humidity"]]


def city_map():
    city_map = folium.Map(
        location=[originY, originX], zoom_start=10, disable_3d=True)
    city_map.add_child(folium.LatLngPopup())
    # city_map.save(
    #     r"E:\PolimiCourseFiles\MyCourses\20202021semester2\SE4geoinformatics\gitProject\Group1_Project\iUrban\templates\map\cityMap.html")
    return city_map


# city_map()


def city_map1():
    city_map = folium.Map(
        location=[originY, originX], zoom_start=10, disable_3d=True)
    city_map.add_child(folium.LatLngPopup())
    city_map.save(
        r"E:\PolimiCourseFiles\MyCourses\20202021semester2\SE4geoinformatics\gitProject\Group1_Project\iUrban\templates\map\cityMap.html")
    return city_map


# city_map1()


def marker():
    markmap = city_map()
    colorlist = ['#ffffff', '#b6f6ff', '#6eedfe', '#25e4ff', '#00e6f1', '#19ffbe', '#46fe9c',
                 '#f6fa0f', '#ffde00', '#fbae00', '#ff7f00', '#ff5300', '#fe2200', '#ef0602', '#c20000', '#950101', '#640002']
    colorbar = branca.colormap.StepColormap(
        colorlist, vmin=df.humidity.min(), vmax=df.humidity.max(), caption='humidity')
    for i in range(len(X)):
        folium.Circle(
            location=[Y[i], X[i]],
            radius=2,
            popup=df.pp[i],
            color=colorbar(df.humidity[i]),
            fill=True,
            fill_opacity=0.5
        ).add_to(markmap)
    markmap.add_child(folium.LatLngPopup())
    markmap.add_child(colorbar)
    markmap.save(r"E:\PolimiCourseFiles\MyCourses\20202021semester2\SE4geoinformatics\gitProject\Group1_Project\iUrban\templates\map\markMap.html")
    return markmap


# marker()


def heatmap():
    heatmap = city_map()
    HeatMap(data).add_to(heatmap)
    heatmap.add_child(folium.LatLngPopup())
    heatmap.save(r'E:\PolimiCourseFiles\MyCourses\20202021semester2\SE4geoinformatics\gitProject\Group1_Project\iUrban\templates\map\heatMap.html')
    return heatmap


# heatmap()


def clustered():
    clustermap = city_map()
    marker_cluster = MarkerCluster().add_to(clustermap)
    for i in range(len(X)):
        folium.Marker(
            location=[Y[i], X[i]],
            icon=None,
            popup=df.pp[i],
        ).add_to(marker_cluster)
    clustermap.add_child(marker_cluster)
    clustermap.add_child(folium.LatLngPopup())
    clustermap.save(
        r"E:\PolimiCourseFiles\MyCourses\20202021semester2\SE4geoinformatics\gitProject\Group1_Project\iUrban\templates\map\clusterMap.html")
    return clustermap


# clustered()


def trade(queryName):
    queryName = queryName
    linedata = df.loc[df['name'] == queryName]
    linedata = linedata[["date", "time", "latitude", "longitude"]]
    datelist = linedata.date
    timelist = linedata.time
    listdata = []
    for i in range(len(datelist)):
        meta = [datelist.iloc[i] + ' ' + timelist.iloc[i],
                linedata.iloc[i, 2], linedata.iloc[i, 3]]
        listdata.append(meta)
    loc = []
    listdata = sorted(listdata, key=lambda t: datetime.strptime(
        t[0], '%d/%m/%Y %H:%M:%S'))
    for i in range(len(linedata)):
        loc.append([listdata[i][1], listdata[i][2]])
    trademap = city_map()
    folium.PolyLine(
        loc,
        weight=4,
        color='red',
        opacity=0.8,
    ).add_to(trademap)

    folium.Marker(loc[0], popup='<b>Starting Point</b>').add_to(trademap)
    folium.Marker(loc[-1], popup='<b>End Point</b>').add_to(trademap)
    trademap.add_child(folium.LatLngPopup())
    trademap.save(
        r"E:\PolimiCourseFiles\MyCourses\20202021semester2\SE4geoinformatics\gitProject\Group1_Project\iUrban\templates\map\tradeMap.html")
    return trademap

# trade()


def polygon():
    poly_map = gp.GeoDataFrame.from_file(
        r"E:\PolimiCourseFiles\MyCourses\20202021semester2\SE4geoinformatics\gitProject\Group1_Project\iUrban\Data\selected.shp", encoding='utf-8')
    Poly_map = city_map()
    # Poly_map.choropleth(
    #         geo_data=poly_map,
    #         key_on= 'feature.properties.NAME_1',
    #         fill_color='Red',
    #         fill_opacity=0.05,
    #         line_opacity=0.2)
    for _, r in poly_map.iterrows():
        # without simplifying the representation of each borough, the map might not be displayed
        # sim_geo = gpd.GeoSeries(r['geometry'])
        sim_geo = gp.GeoSeries(r['geometry']).simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j,
                               style_function=lambda x: {'fillColor': 'orange'})
        folium.Popup(r['NAME_1']).add_to(geo_j)
        geo_j.add_to(Poly_map)
    colorbar = branca.colormap.StepColormap(
        colorlist, vmin=df.humidity.min(), vmax=df.humidity.max(), caption='humidity')
    for i in range(len(X)):
        folium.Circle(
            location=[Y[i], X[i]],
            radius=2,
            popup=df.pp[i],
            color=colorbar(df.humidity[i]),
            fill=True,
            fill_opacity=0.5
        ).add_to(Poly_map)

    Poly_map.add_child(folium.LatLngPopup())
    Poly_map.add_child(colorbar)
    Poly_map.save(
        r"E:\PolimiCourseFiles\MyCourses\20202021semester2\SE4geoinformatics\gitProject\Group1_Project\iUrban\templates\map\polyMap.html")
    return Poly_map


# polygon()


def geo_code():
    geocodemap = city_map()
    colorbar = branca.colormap.StepColormap(colorlist, vmin=df.humidity.min(), vmax=df.humidity.max(),
                                            caption='humidity')
    for i in range(len(X)):
        folium.Circle(
            location=[Y[i], X[i]],
            radius=2,
            popup=df.pp[i],
            color=colorbar(df.humidity[i]),
            fill=True,
            fill_opacity=0.5
        ).add_to(geocodemap)
    position = gp.tools.geocode(
        'Larco Museum', 'Nominatim', user_agent='myuseragent')
    buffer = position.to_crs(epsg=7855).buffer(3000).to_crs(epsg=4326)
    folium.GeoJson(buffer).add_to(geocodemap)
    folium.GeoJson(position, tooltip=folium.GeoJsonTooltip(
        ['address'])).add_to(geocodemap)
    geocodemap.add_child(folium.LatLngPopup())
    geocodemap.add_child(colorbar)
    geocodemap.save(
        r"E:\PolimiCourseFiles\MyCourses\20202021semester2\SE4geoinformatics\gitProject\Group1_Project\iUrban\templates\map\geocodeMap.html")
    return geocodemap


geo_code()

# def convert_toGJ(a):
#     datag = gp.read_file(a)
#     datag.to_file('output',driver="GeoJSON", encoding='utf-8')
#     return data


# def spatial_join():
#     # shpjs = convert_toGJ('selected.shp')
#     poly_map = gp.GeoDataFrame.from_file("selected.shp", encoding='utf-8')
#     Poly_map = city_map()
#     Poly_map.choropleth(
#         geo_data=poly_map,
#         key_on='feature.properties.NAME_1',
#         fill_color='Red',
#         fill_opacity=0.05,
#         line_opacity=0.2)
#     gdf = gp.GeoDataFrame(
#         df, geometry=gp.points_from_xy(df.longitude, df.latitude))
#     statistic = gp.sjoin(poly_map, gdf, how='inner',
#                          op='intersects').groupby('NAME_3')


# spatial_join()
