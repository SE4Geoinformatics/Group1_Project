# import packages
from sqlalchemy import create_engine
import pandas as pd
import geopandas as gpd
import time

#setup db connection (generic connection path to be update with your credentials: 'postgresql://user:password@localhost:5432/mydatabase')
engine = create_engine(
    'postgresql://postgres:postgresql@localhost:5432/iUrbanDB')

# read the dataframe from a postgreSQL table
df_sql = pd.read_sql_table('tdata', engine)

# 2016-03-20 11:45:39 == %Y-%m-%d %H:%M:%S
timeNow = time.strftime("%Y_%m_%d", time.localtime())
fileName = '~/Downloads/environmental_tdata_' + timeNow


def save_file_to_csv():
    df_sql.to_csv(fileName + '.csv')
    return


def save_file_to_json():
    df_sql.to_json(fileName + '.json')
    return


def save_file_to_txt():
    df_sql.to_csv(fileName + '.txt')
    return


