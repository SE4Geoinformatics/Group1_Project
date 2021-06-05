# -*- coding: utf-8 -*-
"""
Created on Sat 24/05/2021

@author: Group 1
"""

from psycopg2 import connect
from psycopg2.extras import execute_batch
from getdata import df


def insertManyOperate():
    conn = connect(host='localhost',port='5432',dbname='iUrbanDB',user='postgres',password='postgre')
    cur = conn.cursor()
    df_columns = list(df.columns)
    # create (col1,col2,...)
    columns =",".join(df_columns)

    # create VALUES('%s', '%s",...) one '%s' per column
    values ="VALUES({})".format(",".join(["%s" for _ in df_columns]))

    #create INSERT INTO table (columns) VALUES('%s',...)
    insert_stmt ="INSERT INTO {} ({}) {}".format('tdata',columns,values)

    execute_batch(cur, insert_stmt, df.values)
    conn.commit()
    cur.close()

    print('insert many records into public.memmber successfully')

insertManyOperate()