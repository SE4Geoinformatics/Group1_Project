#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 00:21:35 2021

@author: Song Xiangyang
"""

from psycopg2 import connect, DatabaseError
from dbConfig import config
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

def connect_db():
    # # use the dbConfig.txt

    # # use this code in VS Code
    myFile = open("E:\\PolimiCourseFiles\\MyCourses\\20202021semester2\\SE4geoinformatics\\gitProject\\Group1_Project\\iUrban\\dbConfig.txt", "r", encoding='utf-8')

    # # use this code in Spyder
    # myFile = open("dbConfig.txt", "r", encoding='utf-8')

    connStr = myFile.readline()
    conn = connect(connStr)
    return conn



    # # use the dbConfig.py
    # params = config()    
    # print('Connecting to the PostgreSQL database...')
    # conn = connect(**params)
    # return conn



cleanup = (
    'DROP TABLE IF EXISTS TUser CASCADE',
    'DROP TABLE IF EXISTS TData',
    'DROP TABLE IF EXISTS TComment',
)

commands = (
    """
    CREATE TABLE TUser (
        user_id SERIAL PRIMARY KEY,
        user_name VARCHAR(255) UNIQUE NOT NULL,
        user_password VARCHAR(255) NOT NULL
        )
    """,
    """
    CREATE TABLE TData (
        data_id SERIAL PRIMARY KEY,
        author_id INTEGER NOT NULL,
        # title VARCHAR(255) NOT NULL, 
        created_date TIMESTAMP DEFAULT NOW(), 
        name VARCHAR(255) NOT NULL,
        date VARCHAR(255) NOT NULL,
        time VARCHAR(255) NOT NULL,            
        latitude VARCHAR(255) NOT NULL,
        longitude VARCHAR(255) NOT NULL,
        average_noise_level VARCHAR(255) NOT NULL,
        average_light_intensity VARCHAR(255) NOT NULL,
        wind_direction VARCHAR(255) NOT NULL,
        wind_speed VARCHAR(255) NOT NULL,
        cloud_cover VARCHAR(255) NOT NULL,        
        cloud_type VARCHAR(255) NOT NULL,
        cloud_photo_id VARCHAR(255) NOT NULL,
        visibility VARCHAR(255) NOT NULL,
        traffic_count VARCHAR(255) NOT NULL,
        temperature VARCHAR(255) NOT NULL,
        humidity VARCHAR(255) NOT NULL,
        collecting_photo_id VARCHAR(255) NOT NULL,        
        note_of_anomaly VARCHAR(255) NOT NULL,
        air_pollution VARCHAR(255) NOT NULL,    
        FOREIGN KEY (author_id) REFERENCES TUser (user_id)
        )
    """,
    """
    CREATE TABLE TComment (
        comment_id SERIAL PRIMARY KEY,
        author_id INTEGER NOT NULL,
        creation TIMESTAMP DEFAULT NOW(),
        title VARCHAR(350) NOT NULL,
        body VARCHAR(500) NOT NULL,
        FOREIGN KEY (author_id) REFERENCES TUser (user_id)
        )
    """
    )

sqlCommands = (
    'INSERT INTO TUser (user_name, user_password) VALUES (%s, %s) RETURNING user_id',
    
    'INSERT INTO TData (author_id, title, name, date, time, longitude, latitude, average_noise_level, average_light_intensity, wind_direction, wind_speed, cloud_cover, cloud_type, cloud_photo_id, visibility, traffic_count, temperature, humidity, collecting_photo_id, note_of_anomaly, air_pollution) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
    
    'INSERT INTO TComment (author_id, title, body) VALUES (%s, %s, %s)'
    )

conn = None
try:
    conn = connect_db()
    # create a cursor
    cur = conn.cursor()
    for command in cleanup:
        cur.execute(command)

    for command in commands:
        cur.execute(command)
        
    # execute a statement
    cur.execute(sqlCommands[0], ('yun', generate_password_hash('123456')))
    cur.execute(sqlCommands[0], ('song', generate_password_hash('123456')))
    cur.execute(sqlCommands[0], ('test', generate_password_hash('123456')))
    userId = cur.fetchone()[0]
    cur.execute(sqlCommands[1], ('1', 'title', 'name', 'date', 'time', 'longitude', 'latitude', 'average_noise_level', 'average_light_intensity', 'wind_direction', 'wind_speed', 'cloud_cover', 'cloud_type', 'cloud_photo_id', 'visibility', 'traffic_count', 'temperature', 'humidity', 'collecting_photo_id', 'note_of_anomaly', 'air_pollution'))
    cur.execute(sqlCommands[1], ('1', 'title', 'name', 'date', 'time', 'longitude', 'latitude', 'average_noise_level', 'average_light_intensity', 'wind_direction', 'wind_speed', 'cloud_cover', 'cloud_type', 'cloud_photo_id', 'visibility', 'traffic_count', 'temperature', 'humidity', 'collecting_photo_id', 'note_of_anomaly', 'air_pollution'))
    cur.execute(sqlCommands[1], ('2', 'title', 'name', 'date', 'time', 'longitude', 'latitude', 'average_noise_level', 'average_light_intensity', 'wind_direction', 'wind_speed', 'cloud_cover', 'cloud_type', 'cloud_photo_id', 'visibility', 'traffic_count', 'temperature', 'humidity', 'collecting_photo_id', 'note_of_anomaly', 'air_pollution'))
    cur.execute(sqlCommands[1], ('2', 'title', 'name', 'date', 'time', 'longitude', 'latitude', 'average_noise_level', 'average_light_intensity', 'wind_direction', 'wind_speed', 'cloud_cover', 'cloud_type', 'cloud_photo_id', 'visibility', 'traffic_count', 'temperature', 'humidity', 'collecting_photo_id', 'note_of_anomaly', 'air_pollution'))
    cur.execute(sqlCommands[1], ('1', 'title', 'name', 'date', 'time', 'longitude', 'latitude', 'average_noise_level', 'average_light_intensity', 'wind_direction', 'wind_speed', 'cloud_cover', 'cloud_type', 'cloud_photo_id', 'visibility', 'traffic_count', 'temperature', 'humidity', 'collecting_photo_id', 'note_of_anomaly', 'air_pollution'))
    cur.execute(sqlCommands[1], ('1', 'title', 'name', 'date', 'time', 'longitude', 'latitude', 'average_noise_level', 'average_light_intensity', 'wind_direction', 'wind_speed', 'cloud_cover', 'cloud_type', 'cloud_photo_id', 'visibility', 'traffic_count', 'temperature', 'humidity', 'collecting_photo_id', 'note_of_anomaly', 'air_pollution'))
    cur.execute(sqlCommands[1], ('2', 'title', 'name', 'date', 'time', 'longitude', 'latitude', 'average_noise_level', 'average_light_intensity', 'wind_direction', 'wind_speed', 'cloud_cover', 'cloud_type', 'cloud_photo_id', 'visibility', 'traffic_count', 'temperature', 'humidity', 'collecting_photo_id', 'note_of_anomaly', 'air_pollution'))
    cur.execute(sqlCommands[1], ('2', 'title', 'name', 'date', 'time', 'longitude', 'latitude', 'average_noise_level', 'average_light_intensity', 'wind_direction', 'wind_speed', 'cloud_cover', 'cloud_type', 'cloud_photo_id', 'visibility', 'traffic_count', 'temperature', 'humidity', 'collecting_photo_id', 'note_of_anomaly', 'air_pollution'))
    cur.execute(sqlCommands[1], ('1', 'title', 'name', 'date', 'time', 'longitude', 'latitude', 'average_noise_level', 'average_light_intensity', 'wind_direction', 'wind_speed', 'cloud_cover', 'cloud_type', 'cloud_photo_id', 'visibility', 'traffic_count', 'temperature', 'humidity', 'collecting_photo_id', 'note_of_anomaly', 'air_pollution'))
    cur.execute(sqlCommands[1], ('1', 'title', 'name', 'date', 'time', 'longitude', 'latitude', 'average_noise_level', 'average_light_intensity', 'wind_direction', 'wind_speed', 'cloud_cover', 'cloud_type', 'cloud_photo_id', 'visibility', 'traffic_count', 'temperature', 'humidity', 'collecting_photo_id', 'note_of_anomaly', 'air_pollution'))
    cur.execute(sqlCommands[1], ('2', 'title', 'name', 'date', 'time', 'longitude', 'latitude', 'average_noise_level', 'average_light_intensity', 'wind_direction', 'wind_speed', 'cloud_cover', 'cloud_type', 'cloud_photo_id', 'visibility', 'traffic_count', 'temperature', 'humidity', 'collecting_photo_id', 'note_of_anomaly', 'air_pollution'))
    cur.execute(sqlCommands[1], ('2', 'title', 'name', 'date', 'time', 'longitude', 'latitude', 'average_noise_level', 'average_light_intensity', 'wind_direction', 'wind_speed', 'cloud_cover', 'cloud_type', 'cloud_photo_id', 'visibility', 'traffic_count', 'temperature', 'humidity', 'collecting_photo_id', 'note_of_anomaly', 'air_pollution'))
    cur.execute(sqlCommands[1], ('1', 'title', 'name', 'date', 'time', 'longitude', 'latitude', 'average_noise_level', 'average_light_intensity', 'wind_direction', 'wind_speed', 'cloud_cover', 'cloud_type', 'cloud_photo_id', 'visibility', 'traffic_count', 'temperature', 'humidity', 'collecting_photo_id', 'note_of_anomaly', 'air_pollution'))
    cur.execute(sqlCommands[1], ('1', 'title', 'name', 'date', 'time', 'longitude', 'latitude', 'average_noise_level', 'average_light_intensity', 'wind_direction', 'wind_speed', 'cloud_cover', 'cloud_type', 'cloud_photo_id', 'visibility', 'traffic_count', 'temperature', 'humidity', 'collecting_photo_id', 'note_of_anomaly', 'air_pollution'))
    cur.execute(sqlCommands[1], ('2', 'title', 'name', 'date', 'time', 'longitude', 'latitude', 'average_noise_level', 'average_light_intensity', 'wind_direction', 'wind_speed', 'cloud_cover', 'cloud_type', 'cloud_photo_id', 'visibility', 'traffic_count', 'temperature', 'humidity', 'collecting_photo_id', 'note_of_anomaly', 'air_pollution'))
    cur.execute(sqlCommands[1], ('2', 'title', 'name', 'date', 'time', 'longitude', 'latitude', 'average_noise_level', 'average_light_intensity', 'wind_direction', 'wind_speed', 'cloud_cover', 'cloud_type', 'cloud_photo_id', 'visibility', 'traffic_count', 'temperature', 'humidity', 'collecting_photo_id', 'note_of_anomaly', 'air_pollution'))
    cur.execute(sqlCommands[1], ('1', 'title', 'name', 'date', 'time', 'longitude', 'latitude', 'average_noise_level', 'average_light_intensity', 'wind_direction', 'wind_speed', 'cloud_cover', 'cloud_type', 'cloud_photo_id', 'visibility', 'traffic_count', 'temperature', 'humidity', 'collecting_photo_id', 'note_of_anomaly', 'air_pollution'))
    cur.execute(sqlCommands[1], ('1', 'title', 'name', 'date', 'time', 'longitude', 'latitude', 'average_noise_level', 'average_light_intensity', 'wind_direction', 'wind_speed', 'cloud_cover', 'cloud_type', 'cloud_photo_id', 'visibility', 'traffic_count', 'temperature', 'humidity', 'collecting_photo_id', 'note_of_anomaly', 'air_pollution'))
    cur.execute(sqlCommands[1], ('2', 'title', 'name', 'date', 'time', 'longitude', 'latitude', 'average_noise_level', 'average_light_intensity', 'wind_direction', 'wind_speed', 'cloud_cover', 'cloud_type', 'cloud_photo_id', 'visibility', 'traffic_count', 'temperature', 'humidity', 'collecting_photo_id', 'note_of_anomaly', 'air_pollution'))
    cur.execute(sqlCommands[1], ('2', 'title', 'name', 'date', 'time', 'longitude', 'latitude', 'average_noise_level', 'average_light_intensity', 'wind_direction', 'wind_speed', 'cloud_cover', 'cloud_type', 'cloud_photo_id', 'visibility', 'traffic_count', 'temperature', 'humidity', 'collecting_photo_id', 'note_of_anomaly', 'air_pollution'))
    cur.execute(sqlCommands[2], ('1', 'Please!', 'leave a comment'))
    cur.execute(sqlCommands[2], ('1', 'Please!', 'leave a comment'))
    cur.execute(sqlCommands[2], ('2', 'Please!', 'leave a comment'))
    cur.execute(sqlCommands[2], ('2', 'Please!', 'leave a comment'))

    # print(cur.fetchall())
    cur.close()

except (Exception, DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.commit()
        conn.close()
        print('Database connection closed.')
