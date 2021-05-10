# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 22:52:38 2021

@author: Group 1
"""
#!/usr/bin/python
from flask import (
    Flask,
    render_template,
    session,
    redirect,
    url_for,
    request,
    flash
)

from psycopg2 import connect

app = Flask(__name__, template_folder='templates')

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'


def connect_db():
    # use this code in VS Code
    # myFile = open("E:\\PolimiCourseFiles\\MyCourses\\20202021semester2\\SE4geoinformatics\\\gitProject\\Group1_Project\\iUrban\\dbConfig.txt", "r", encoding='utf-8')

    # use this code in Spyder
    myFile = open("dbConfig.txt", "r", encoding='utf-8')

    connStr = myFile.readline()
    conn = connect(connStr)
    return conn


@app.route('/home', methods=('GET', 'POST'))
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5001,
        debug=True)
