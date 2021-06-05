# import packages
import requests
import json
import pandas as pd
import geopandas as gpd
import re

from psycopg2 import connect
# from sqlalchemy import create_engine


def connect_db():
    # # use the dbConfig.txt

    # # # use this code in VS Code
    myFile = open("E:\\PolimiCourseFiles\\MyCourses\\20202021semester2\\SE4geoinformatics\\gitProject\\Group1_Project\\iUrban\\dbConfig.txt", "r", encoding='utf-8')
    # myFile = open("E:\\path in your computer\\Group1_Project\\iUrban\\dbConfig.txt", "r", encoding='utf-8')

    # # # use this code in Spyder
    # # myFile = open("dbConfig.txt", "r", encoding='utf-8')

    connStr = myFile.readline()
    conn = connect(connStr)
    return conn


def UpdateFromEP5():
    # send the request
    response = requests.get(
        'https://five.epicollect.net/api/export/entries/san-silvestre-geography-ia-2020?per_page=50')

    # store the raw text of the response in a variable
    raw_data = response.text

    # parse the raw text response
    data = json.loads(raw_data)

    data = (data['data']['entries'])

    # from JSON to Pandas DataFrame
    #data_df = pd.json_normalize(data['data']['entries'])
    i = 0
    for raw in data:
        # print(raw['2_Location']['longitude'])
        author_id = 1
        created_date = raw['created_at']
        name = raw['1_Name']
        date = raw['3_Date']
        time = raw['4_Time']
        latitude = raw['2_Location']['latitude']
        longitude = raw['2_Location']['longitude']
        # int
        average_noise_level = raw['5_Average_noise_leve']
        # int
        average_light_intensity = raw['6_Average_light_inte']
        wind_direction = raw['7_Wind_direction']
        # wind_speed = raw['8_Wind_speed_Beaufor']
        if not raw['8_Wind_speed_Beaufor']:
            wind_speed = 0
        else:
            wind_speed = raw['8_Wind_speed_Beaufor']
        cloud_cover = raw['9_Cloud_cover']
        cloud_type = raw['10_Cloud_type']
        cloud_photo_id = raw['11_Photo_of_cloud_co']

        # visibility = raw['12_Visibility']
        if not raw['12_Visibility']:
            visibility = 0
        else:
            visibility = raw['12_Visibility']

        # traffic_count = raw['13_Traffic_count']
        if not raw['13_Traffic_count']:
            traffic_count = 0
        else:
            traffic_count = raw['13_Traffic_count']

        # temperature = raw['14_Temperature']
        if not raw['14_Temperature']:
            temperature = 0
        else:
            temperature = raw['14_Temperature']

        # humidity = raw['15_Humidity']
        if not raw['15_Humidity']:
            humidity = 0
        else:
            humidity = raw['15_Humidity']

        note_of_anomaly = raw['17_Make_a_note_of_an']

        # air_pollution
        if not raw['18_Air_pollution_num']:
            air_pollution = 0
        else:
            air_pollution = raw['18_Air_pollution_num']

        conn = connect_db()
        cur = conn.cursor()  # create a cursor
        cur.execute(
            'SELECT * FROM TData WHERE latitude = %s and longitude = %s and date = %s and time = %s and name = %s', (
                latitude, longitude, date, time, name,)
        )
        data_id = cur.fetchone()
        #cur.close()  # close this cursor
        conn.commit()

        if data_id is None:
            # conn = connect_db()
            # cur = conn.cursor()  # create a cursor
            cur.execute(
                'INSERT INTO TData (author_id, created_date, name, date, time, latitude, longitude, average_noise_level, average_light_intensity, wind_direction, wind_speed, cloud_cover, cloud_type, cloud_photo_id, visibility, traffic_count, temperature, humidity, note_of_anomaly, air_pollution) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (
                    author_id, created_date, name, date, time, latitude, longitude, average_noise_level, average_light_intensity, wind_direction, wind_speed, cloud_cover, cloud_type, cloud_photo_id, visibility, traffic_count, temperature, humidity, note_of_anomaly, air_pollution)
            )
            #cur.close()
            conn.commit()
            i = i+1
        else:
            # if date> data_id[4] and time > data_id[5]:
            #     # conn = connect_db()
            #     # cur = conn.cursor()  # create a cursor
            #     # cur.execute(
            #     #     'SELECT * FROM TData WHERE latitude = %s and longitude = %s and date = %s and time = %s and name = %s', (latitude, longitude, date, time, name,)
            #     # )
            #     # data_id = cur.fetchone()
            #     # cur.close()  # close this cursor
            #     # conn.commit()
            #     continue
            # else:
            #     print('数据已存在')
            #     continue
            print('This data already exists')
            continue
    print('Close the db link')
    cur.close()
    print('Return the value of updating count')
    return i
