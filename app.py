# app.py

from flask import Flask, g, redirect, render_template, request, jsonify, make_response, url_for
from flask_socketio import SocketIO, emit
import sqlite3
from urllib.parse import quote, unquote
from flask_mysqldb import MySQL
import secrets
import json
from threading import Thread,Event
import time
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination
from models import db,Mypot
from threading import Lock
from func import *

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
#DATABASE = '../Database_test/dionaea.sqlite'

thread = None
thread_lock = Lock()

password_encoded = quote("Mypot@123")
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://mypot@localhost/mypot?password={password_encoded}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'mypot'
app.config['MYSQL_PASSWORD'] = 'Mypot@123'
app.config['MYSQL_DB'] = 'mypot'

mysql = MySQL(app)
db.init_app(app)
socketio = SocketIO(app)  
stop_event = Event()

@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            print("Current thread Start:", thread)
            thread = socketio.start_background_task(background_thread)


@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

def background_thread(sort_by=None, intable_value=None):
    print("Query Database Limit 20")
    with app.app_context():
        while not stop_event.is_set():
            response_data = Get_SortDB(sort_by=sort_by,intable_value=intable_value)
            #print('----------------------------------Emit data-------------------------------------')
            socketio.emit('updateResponse_data', response_data, namespace='')
            socketio.sleep(1)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dionaea/chart')
def dionaea_chart():
    return render_template('/dionaea/Chart_1.html')

@app.route('/dionaea/table')
def dionaea_table():
    return render_template('/dionaea/table_1.html')

@app.route('/dionaea')
def dionaea_index():
    return render_template('/dionaea/index.html')

@app.route('/cowrie')
def cowrie_index():
    return render_template('/cowrie/index.html')

@app.route('/Monitor')
def Monitor():
    return render_template('Monitor.html') 

@app.route('/Monitor', methods=['POST'])
def submit_filter():
    sort_by = request.form['SORTBY']
    intable_value = request.form['intable_value']
    print("Sort by:", sort_by)
    print("Intable value:", intable_value)
    
    global thread
    with thread_lock:
        if thread:  # ตรวจสอบว่าเธรดเก่ายังมีอยู่หรือไม่
            stop_event.set()  # เซ็ต stop_event เป็น True เพื่อให้เธรดเก่าหยุดทำงาน
            thread.join()  # รอให้เธรดเก่าจบการทำงานก่อน
            thread = None  # ลบเธรดเก่าทิ้ง
        stop_event.clear()  # เซ็ต stop_event เป็น False เพื่อเตรียมสำหรับเธรดใหม่
        
        
        thread = socketio.start_background_task(lambda: background_thread(sort_by, intable_value))
        print("Current thread Switch:", thread)

    return redirect(url_for('Monitor'))
    

@app.route('/History')
def History():
    data = Get_db()
    return render_template('History.html',data=data) 



if __name__ == '__main__':
    socketio.run(app,debug=True)