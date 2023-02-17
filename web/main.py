from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
from functions import storeTemperature, getTemperatureData, getCurrentTemperature, checkDBforUser, getAllUsers, getUser, getTargetedTemperature, storeTargetedTemperature, getDevicesStatus, storeDevicesStatus, checkIfEmailExists, registerUser

from hashlib import sha256
import datetime as dt


app = Flask(__name__)
# define secret key for session
app.secret_key = '_5#y2L"aF4Qea43sseze\n\xec]/'

# mysql database parameters
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'app'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'baza'

# access database
mysql = MySQL(app)

# starting page with temperature data


@app.route('/')
def index():
    if 'username' in session:
        temperatures1, dates1 = getTemperatureData(
            mysql, table='temperature1')
        temperatures2, dates2 = getTemperatureData(
            mysql, table='temperature2')
        user = getUser(mysql, session)
        return render_template('index.html', temperatures1=temperatures1, dates1=dates1, user=user, temperatures2=temperatures2, dates2=dates2), 201

    return redirect(url_for('login')), 303


# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html'), 201
    elif request.method == 'POST':
        user, email = checkDBforUser(mysql, request, sha256)
        if user:
            # user is valid to login
            session['username'] = email
            return redirect(url_for('index')), 303
        else:
            return render_template('login.html', error='Incorrect email or password'), 401


# registration page
@app.route('/register-another-user', methods=['GET', 'POST'])
def registracija():
    user = getUser(mysql, session)
    if request.method == 'GET':
        users = getAllUsers(mysql)
        return render_template('register_another_user.html',  users=users, user=user), 201
    elif request.method == 'POST':
        isEmailAlreadyRegisterd = checkIfEmailExists(mysql, request)
        if isEmailAlreadyRegisterd:
            users = getAllUsers(mysql)
            return render_template('register_another_user.html', error='This email is already in use', users=users, user=user), 409
        else:
            registerUser(mysql, request)
            users = getAllUsers(mysql)
            return render_template('register_another_user.html', users=users, user=user), 201


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index')), 303


# sensor 1
@app.route("/temp_sensor_one", methods=["GET", "POST"],)
def temperature_sensor1():
    if request.method == "GET":
        temperature1, isSensorConnected = getCurrentTemperature(
            mysql, dt, table='temperature1')
        if isSensorConnected:
            return str(temperature1)
        else:
            return 'Sensor not connected', 404
    elif request.method == "POST":
        value = request.args.get("value")
        if value:
            storeTemperature(mysql, value, table='temperature1')
            return 'Value stored'
        return 'Value not recieved', 404


# sensor 2
@app.route("/temp_sensor_two", methods=["GET", "POST"])
def temperature_sensor2():
    if request.method == "GET":
        temperature2, isSensorConnected = getCurrentTemperature(
            mysql, dt, table='temperature2')
        if isSensorConnected:
            return str(temperature2)
        else:
            return 'Sensor not connected', 404
    elif request.method == "POST":
        value = request.args.get("value")
        if value:
            storeTemperature(mysql, value, table='temperature2')
            return 'Value stored'
        return 'Value not recieved', 404


@app.route("/targeted_temperature", methods=["GET", "POST"],)
def targeted_temp():
    if request.method == "GET":
        targetedTemperature = getTargetedTemperature(mysql)
        return str(targetedTemperature)
    elif request.method == "POST":
        storeTargetedTemperature(mysql, request)
        targetedTemperature = getTargetedTemperature(mysql)
        return str(targetedTemperature)


@app.route("/devices", methods=["GET", "POST"])
def device_status():
    if request.method == "GET":
        devicesStatus, areDevicesConnected = getDevicesStatus(mysql, dt)
        if (areDevicesConnected):
            return devicesStatus, 201
        else:
            return 'Devices not connected', 404
    elif request.method == "POST":
        storeDevicesStatus(mysql, request)
        devicesStatus, areDevicesConnected = getDevicesStatus(mysql, dt)
        if (areDevicesConnected):
            return devicesStatus, 201
        else:
            return 'Devices not connected', 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
