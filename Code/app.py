# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 22:18:54 2021

@author: Song Xiangyang
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
