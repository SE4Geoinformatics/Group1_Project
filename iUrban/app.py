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
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from werkzeug.exceptions import abort

from psycopg2 import connect

from dbConfig import config

app = Flask(__name__, template_folder='templates')

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            # params = config()
            # conn = connect(**params)
            conn = connect_db()
            cur = conn.cursor()
            cur.execute(
                'SELECT user_id FROM TUser WHERE user_name = %s', (username,))
            if cur.fetchone() is not None:
                error = 'User {} is already registered.'.format(username)
                cur.close()

        if error is None:
            # params = config()
            # conn = connect(**params)
            conn = connect_db()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO TUser (user_name, user_password) VALUES (%s, %s)',
                (username, generate_password_hash(password))
            )
            cur.close()
            conn.commit()
            return redirect(url_for('index'))

        flash(error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        conn = connect_db()
        cur = conn.cursor()  # create a cursor
        cur.execute(
            'SELECT * FROM TUser WHERE user_name = %s', (username,)
        )
        user = cur.fetchone()
        cur.close()  # close this cursor
        conn.commit()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('index'))

        flash(error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/base')
def base():
    return render_template('base.html')


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/table')
def table():
    conn = connect_db()
    cur = conn.cursor()  # create a cursor
    cur.execute(
        """SELECT * FROM TData"""
    )

    tData = cur.fetchall()
    cur.close()
    conn.commit()

    return render_template('table.html', page_title='Table', tData=tData)

@app.route('/comment/<int:data_id>')
def comment(data_id):
    data_id = data_id
    conn = connect_db()
    cur = conn.cursor()  # create a cursor
    cur.execute(
        'SELECT * FROM TComment WHERE data_id = %s', (data_id,)
    )

    tComment = cur.fetchall()
    cur.close()
    conn.commit()

    return render_template('comment.html', page_title=data_id, tComment=tComment)

if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5001,
        debug=True)
