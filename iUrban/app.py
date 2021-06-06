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
    flash,
    g
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from werkzeug.exceptions import abort

from psycopg2 import connect

from dbConfig import config


from tkinter import messagebox

from bokeh.plotting import figure
from bokeh.embed import components
from flask import Flask, request, render_template, abort, Response
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show, output_file

from DataPackage import updateDataFromEP5, exportData

app = Flask(__name__, template_folder='templates')

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'


def get_dbConn():
    if 'dbConn' not in g:
        myFile = open(
            "E:\\PolimiCourseFiles\MyCourses\\20202021semester2\\SE4geoinformatics\\gitProject\\Group1_Project\\iUrban\\dbConfig.txt", "r", encoding='utf-8')
        connStr = myFile.readline()
        g.dbConn = connect(connStr)

    return g.dbConn


def close_dbConn():
    if 'dbConn' in g:
        g.dbComm.close()
        g.pop('dbConn')


def connect_db():
    # # use the dbConfig.txt

    # # # use this code in VS Code
    myFile = open("E:\\PolimiCourseFiles\MyCourses\\20202021semester2\\SE4geoinformatics\\gitProject\\Group1_Project\\iUrban\\dbConfig.txt", "r", encoding='utf-8')
    # myFile = open("E:\\path in your computer\\Group1_Project\\iUrban\\dbConfig.txt", "r", encoding='utf-8')

    # # # use this code in Spyder
    # # myFile = open("dbConfig.txt", "r", encoding='utf-8')

    connStr = myFile.readline()
    conn = connect(connStr)
    return conn

    #*************************************************************
    # # use the dbConfig.py
    # params = config()
    # print('Connecting to the PostgreSQL database...')
    # conn = connect(**params)
    # return conn


def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM TUser WHERE user_id = %s', (user_id,)
        )
        g.user = cur.fetchone()
        cur.close()
        conn.commit()
    if g.user is None:
        return False
    else:
        return True


@app.route('/about', methods=['GET'])
def aboutPage():
    return render_template('about/about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_email = request.form.get('user_email')
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
                'INSERT INTO TUser (user_name, user_password, user_email) VALUES (%s, %s, %s)',
                (username, generate_password_hash(password), user_email)
            )
            cur.close()
            conn.commit()
            return redirect(url_for('index'))

    else:
        error = 'Please register!'

    flash(error)
    return render_template('index.html')


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
            load_logged_in_user()
            return redirect(url_for('index'))

    else:
        error = 'Please loging!'

    flash(error)
    return render_template('index.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/resetPassword', methods=['GET', 'POST'])
def resetPassword():
    if load_logged_in_user():
        session.clear()
        return render_template('resetPassword.html')
    else:
        return render_template('resetPassword.html')


@app.route('/userProfile', methods=['GET', 'POST'])
def userProfile():
    if load_logged_in_user():
        user_id = session.get('user_id')

        conn = connect_db()
        cur = conn.cursor()  # create a cursor
        cur.execute(
            'SELECT user_name, user_email FROM TUser WHERE user_id = %s', (
                user_id,)
        )
        TUser = cur.fetchall()
        cur.close()  # close this cursor
        conn.commit()

        if request.method == 'POST':
            newpassword1 = request.form.get('newpassword1')
            newpassword2 = request.form.get('newpassword2')

            if newpassword1 == newpassword2:
                conn = connect_db()
                cur = conn.cursor()  # create a cursor
                cur.execute(
                    'UPDATE TUser SET user_password=%s WHERE user_id = %s', (
                        newpassword2, user_id,)
                )
                # TUser = cur.fetchall()
                cur.close()  # close this cursor
                conn.commit()

                error = 'Edit successfully'
                flash(error)
                return render_template('userProfile.html', TUser=TUser)
            else:
                error = 'Two password entries are inconsistent!'
                flash(error)
                return render_template('userProfile.html', TUser=TUser)
        else:
            return render_template('userProfile.html', TUser=TUser)
    else:
        error = 'Please login!'
        flash(error)
        return render_template('index.html')


@app.route('/deleteAccount', methods=['GET', 'POST'])
def deleteAccount():
    if load_logged_in_user():
        user_id = session.get('user_id')

        conn = connect_db()
        cur = conn.cursor()  # create a cursor
        cur.execute(
            'DELETE FROM TComment WHERE author_id = %s', (user_id,)
        )
        cur.execute(
            'DELETE FROM TComment WHERE data_id in (select data_id from TData where author_id = %s)', (
                user_id,)
        )
        cur.execute(
            'DELETE FROM TData WHERE author_id = %s', (user_id,)
        )
        cur.execute(
            'DELETE FROM TUser WHERE user_id = %s', (user_id,)
        )
        cur.close()  # close this cursor
        conn.commit()

    session.clear()
    return render_template('index.html')


@app.route('/base')
def base():    
    return render_template('index.html')


@app.route('/test')
def test():

    # return '''
    # <form method="post">
    # <p><input type=text name=username>
    # <p><input type=submit value=Login>
    # </form>
    # '''
    return render_template('test.html')


@app.route('/')
@app.route('/index')
def index():
    conn = connect_db()
    cur = conn.cursor()  # create a cursor
    cur.execute(
        'select count(data_id) from TData'
    )
    dataCount = cur.fetchone()[0]
    cur.close()  # close this cursor
    conn.commit()
    return render_template('index.html', dataCount=dataCount)


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


@app.route('/queryData', methods=('GET', 'POST'))
def queryData():
    if request.method == 'POST':
        dtitle = request.form.get('dtitle')
        dcondition = request.form.get('dcondition')
        dpara = request.form.get('dpara')

        conn = connect_db()
        cur = conn.cursor()  # create a cursor
        cur.execute(
            '''SELECT * FROM TData WHERE  ''' +
            dtitle + dcondition + '''%s''', (dpara,)
        )

        tData = cur.fetchall()
        cur.close()
        conn.commit()

        return render_template('table.html', page_title='Table', tData=tData)
    else:
        # error = 'Only logged in users can add data!'
        # flash(error)
        return render_template('index.html', page_title='Index')


@app.route('/addData', methods=('GET', 'POST'))
def addData():
    if load_logged_in_user():
        if request.method == 'POST':
            author_id = session['user_id']
            name = request.form.get('name')
            date = request.form.get('date')
            time = request.form.get('time')
            longitude = request.form.get('longitude')
            latitude = request.form.get('latitude')
            average_noise_level = request.form.get('average_noise_level')
            average_light_intensity = request.form.get(
                'average_light_intensity')
            wind_direction = request.form.get('wind_direction')
            wind_speed = request.form.get('wind_speed')
            cloud_cover = request.form.get('cloud_cover')
            cloud_type = request.form.get('cloud_type')
            cloud_photo_id = request.form.get('cloud_photo_id')
            visibility = request.form.get('visibility')
            traffic_count = request.form.get('traffic_count')
            temperature = request.form.get('temperature')
            humidity = request.form.get('humidity')
            note_of_anomaly = request.form.get('note_of_anomaly')
            air_pollution = request.form.get('air_pollution')

            conn = connect_db()
            cur = conn.cursor()  # create a cursor
            cur.execute(
                'INSERT INTO TData (author_id, name, date, time, longitude, latitude, average_noise_level, average_light_intensity, wind_direction, wind_speed, cloud_cover, cloud_type, cloud_photo_id, visibility, traffic_count, temperature, humidity, note_of_anomaly, air_pollution) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (
                    author_id, name, date, time, longitude, latitude, average_noise_level, average_light_intensity, wind_direction, wind_speed, cloud_cover, cloud_type, cloud_photo_id, visibility, traffic_count, temperature, humidity, note_of_anomaly, air_pollution)
            )
            cur.close()
            conn.commit()
            return redirect(url_for('table'))

        return render_template('addData.html', page_title='Add Data')
    else:
        error = 'Only logged in users can add data!'
        flash(error)
        return render_template('index.html', page_title='Index')


@app.route('/deleteData/<int:data_id>')
def deleteData(data_id):
    data_id = data_id

    conn = connect_db()
    cur = conn.cursor()  # create a cursor
    cur.execute(
        'delete FROM TComment WHERE data_id = %s', (data_id,)
    )
    cur.execute(
        'delete FROM TData WHERE data_id = %s', (data_id,)
    )
    cur.close()
    conn.commit()

    return redirect(url_for('table'))


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

    return render_template('comment.html', page_title=data_id, tComment=tComment, data_id=data_id)


@app.route('/addComment/<int:data_id>', methods=['GET', 'POST'])
def addComment(data_id):
    data_id = data_id
    author_id = session['user_id']
    body = request.form.get('comment_body')

    conn = connect_db()
    cur = conn.cursor()  # create a cursor
    cur.execute(
        'INSERT INTO TComment (author_id, data_id, body) VALUES (%s, %s, %s)', (
            author_id, data_id, body)
    )

    cur.close()
    conn.commit()

    return redirect(url_for('comment', data_id=data_id))


@app.route('/deleteComment/<int:comment_id>/<int:data_id>')
def deleteComment(comment_id, data_id):
    comment_id = comment_id
    data_id = data_id

    conn = connect_db()
    cur = conn.cursor()  # create a cursor
    cur.execute(
        'delete FROM TComment WHERE comment_id = %s', (comment_id,)
    )
    cur.close()
    conn.commit()

    return redirect(url_for('comment', data_id=data_id))


@app.route('/saveData/<saveType>')
def saveData(saveType):
    if load_logged_in_user():
        error = exportData.save_file(saveType)
        flash(error)
        return redirect(url_for('index'))
    else:
        error = 'Please login!'
        flash(error)
        return render_template('index.html')

@app.route('/upEP5')
def upEP5():
    if load_logged_in_user():
        countData = updateDataFromEP5.UpdateFromEP5()
        error = 'Update successfully! Totle update '+ str(countData) +' data'
        flash(error)        
        return redirect(url_for('table'))
    else:
        error = 'Please login!'
        flash(error)
        return render_template('index.html')

@app.route('/graphs/plotting')
def plotting():
    x = [5, 6, 7, 8, 9, 10]
    y = [1, 2, 3, 4, 5, 6]

    plot = figure()
    plot.line(x, y)
    plot.cross(x, y, size=15)

    #Return HTML components to embed a Bokeh plot. The data for the plot is
    #stored directly in the returned HTML
    plot_script, plot_div = components(plot)

    kwargs = {'plot_script': plot_script, 'plot_div': plot_div}
    kwargs['title'] = 'plotting'
    if request.method == 'GET':
        return render_template('graphs/plotting.html', **kwargs)
    abort(404)
    abort(Response('plotting'))


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5001,
        debug=True)
