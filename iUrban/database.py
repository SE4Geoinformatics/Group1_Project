#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 00:21:35 2021

@author: Song Xiangyang
"""

from psycopg2 import connect, DatabaseError
from ConnectDB import connect_db

from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)


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
        user_email varchar(255)
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
        latitude FLOAT(32) NOT NULL,
        longitude FLOAT(32) NOT NULL,
        average_noise_level INTEGER NOT NULL,
        average_light_intensity INTEGER NOT NULL,
        wind_direction VARCHAR(32) NOT NULL,
        wind_speed INTEGER NOT NULL,
        cloud_cover INTEGER NOT NULL,
        cloud_type VARCHAR(32) NOT NULL,
        cloud_photo_id VARCHAR(225),
        visibility INTEGER NOT NULL,
        traffic_count INTEGER NOT NULL,
        temperature INTEGER NOT NULL,
        humidity INTEGER NOT NULL,
        note_of_anomaly VARCHAR(225),
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
    'INSERT INTO TUser (user_name, user_password, user_email) VALUES (%s, %s, %s) RETURNING user_id',

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
    cur.execute(sqlCommands[0], ('admin', generate_password_hash(
        '123456'), 'song@mail.polimi'))
    cur.execute(sqlCommands[0], ('song', generate_password_hash(
        '123456'), 'song@mail.polimi'))
    userId = cur.fetchone()[0]

    # cur.execute(sqlCommands[1], ('1', 'name', 'date', 'time', 'latitude', 'longitude', 'average_noise_level', 'average_light_intensity', 'wind_direction', 'wind_speed', 'cloud_cover', 'cloud_type', 'cloud_photo_id', 'visibility', 'traffic_count', 'temperature', 'humidity', 'note_of_anomaly', 'air_pollution'))

    # cur.execute(sqlCommands[1], (userId, 'macarena valdivia', '23/11/2020', '08:00:00', '-12.102838', '-77.039238', '57', '7164', 'NE', '4', '8', 'stratus', 'cloud_photo_id', '2', '102', '21', '68', 'note_of_anomaly', '9'))

    # cur.execute(sqlCommands[1], (userId, 'song', '24/11/2020', '09:00:00', '-12.102838', '-77.039238', '57', '7164', 'NE', '4', '8', 'stratus', 'cloud_photo_id', '2', '102', '21', '68', 'note_of_anomaly', '9'))

    # cur.execute(sqlCommands[1], (userId, 'ding', '22/11/2020', '12:00:00', '-12.102838', '-77.039238', '50', '7164', 'NE', '4', '9', 'stratus', 'cloud_photo_id', '2', '100', '21', '68', 'note_of_anomaly', '9'))

    # cur.execute(sqlCommands[2], ('1', '1', 'i am admin'))
    # cur.execute(sqlCommands[2], ('1', '1', 'i am admin'))
    # cur.execute(sqlCommands[2], ('2', '1', 'i am song'))
    # cur.execute(sqlCommands[2], ('2', '2', 'i am song'))

    # print(cur.fetchall())
    cur.close()

except (Exception, DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.commit()
        conn.close()
        print('Database connection closed.')
