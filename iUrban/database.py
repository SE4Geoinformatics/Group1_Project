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
    'DROP TABLE IF EXISTS TComment',
    'DROP TABLE IF EXISTS TData',
)

commands = (
    """
    CREATE TABLE TUser (
        user_id SERIAL PRIMARY KEY,
        user_name VARCHAR(20) UNIQUE NOT NULL,
        user_password VARCHAR(255) NOT NULL,
        user_email varchar(30)
        )
    """,

    """
    CREATE TABLE TData (
        data_id SERIAL PRIMARY KEY,
        author_id INTEGER NOT NULL,
        created_date TIMESTAMP DEFAULT NOW(),
        name VARCHAR(50) NOT NULL,
        date VARCHAR(50) NOT NULL,
        time VARCHAR(50) NOT NULL,
        latitude FLOAT(16) NOT NULL,
        longitude FLOAT(16) NOT NULL,
        average_noise_level INTEGER NOT NULL,
        average_light_intensity INTEGER NOT NULL,
        wind_direction VARCHAR(16) NOT NULL,
        wind_speed INTEGER NOT NULL,
        cloud_cover INTEGER NOT NULL,
        cloud_type VARCHAR(16) NOT NULL,
        cloud_photo_id VARCHAR(225),
        visibility INTEGER NOT NULL,
        traffic_count INTEGER NOT NULL,
        temperature INTEGER NOT NULL,
        humidity INTEGER NOT NULL,
        note_of_anomaly VARCHAR(50),
        air_pollution INTEGER,
        FOREIGN KEY (author_id) REFERENCES TUser (user_id)
        )
    """,

    """
    CREATE TABLE TComment (
        comment_id SERIAL PRIMARY KEY,
        author_id INTEGER NOT NULL,
        data_id INTEGER NOT NULL,
        created_date TIMESTAMP DEFAULT NOW(),
        body VARCHAR(50) NOT NULL,
        FOREIGN KEY (data_id) REFERENCES TData (data_id)
        )
    """
)

sqlCommands = (
    'INSERT INTO TUser (user_name, user_password) VALUES (%s, %s) RETURNING user_id',

    'INSERT INTO TData (author_id,  name, date, time, latitude, longitude, average_noise_level, average_light_intensity, wind_direction, wind_speed, cloud_cover, cloud_type, cloud_photo_id, visibility, traffic_count, temperature, humidity, note_of_anomaly, air_pollution) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s)',

    'INSERT INTO TComment (author_id, data_id, body) VALUES (%s, %s, %s)'

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
    cur.execute(sqlCommands[0], ('song', generate_password_hash('123456')))
    cur.execute(sqlCommands[0], ('test', generate_password_hash('123456')))
    userId = cur.fetchone()[0]

    # cur.execute(sqlCommands[1], ('1', 'name', 'date', 'time', 'latitude', 'longitude', 'average_noise_level', 'average_light_intensity', 'wind_direction', 'wind_speed', 'cloud_cover', 'cloud_type', 'cloud_photo_id', 'visibility', 'traffic_count', 'temperature', 'humidity', 'note_of_anomaly', 'air_pollution'))

    cur.execute(sqlCommands[1], (userId, 'macarena valdivia', '23/11/2020', '08:00:00', '-12.102838', '-77.039238', '57', '7164', 'NE', '4', '8', 'stratus', 'cloud_photo_id', '2', '102', '21', '68', 'note_of_anomaly', '9'))
    
    cur.execute(sqlCommands[1], (userId, 'song', '24/11/2020', '09:00:00', '-12.102838', '-77.039238', '57', '7164', 'NE', '4', '8', 'stratus', 'cloud_photo_id', '2', '102', '21', '68', 'note_of_anomaly', '9'))

    cur.execute(sqlCommands[1], (userId, 'ding', '22/11/2020', '12:00:00', '-12.102838', '-77.039238', '50', '7164', 'NE', '4', '9', 'stratus', 'cloud_photo_id', '2', '100', '21', '68', 'note_of_anomaly', '9'))

    cur.execute(sqlCommands[2], ('1', '1', 'leave a comment'))
    cur.execute(sqlCommands[2], ('1', '1', 'leave a comment'))
    cur.execute(sqlCommands[2], ('2', '1', 'leave a comment'))
    cur.execute(sqlCommands[2], ('2', '2', 'leave a comment'))

    # print(cur.fetchall())
    cur.close()

except (Exception, DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.commit()
        conn.close()
        print('Database connection closed.')
