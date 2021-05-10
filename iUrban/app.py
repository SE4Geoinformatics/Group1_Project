# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 22:52:38 2021

@author: Group 1
"""
#!/usr/bin/python
from flask import (
    Flask,
    render_template
)

app = Flask(__name__, template_folder='templates')

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5001,
        debug=True)
