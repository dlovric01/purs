from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from functions import storeTemperature, getTemperatureData, getLastTempFromDB, checkDBforUser, getAllUsers, getUser

from hashlib import sha256

app = Flask(__name__)
# define secret key for session
app.secret_key = '_5#y2L"aF4Qea4sseze\n\xec]/'

# mysql database parameters
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'app'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'baza'

# access database
mysql = MySQL(app)

# starting page with temperature data


@app.route('/', methods=['GET'])
def index():
    if 'username' in session:
        data, temperatures, dates, lastTemp = getTemperatureData(
            mysql, session)
        user = getUser(mysql, session)
        return render_template('index.html', data=data, temperatures=temperatures, dates=dates, lastTemp=lastTemp, user=user)

    return redirect(url_for('login')), 303


# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        user, email = checkDBforUser(mysql, request, sha256)
        if user:
            # user is valid to login
            session['username'] = email
            return redirect(url_for('index')), 303
        else:
            return render_template('login.html', error='Incorrect email or password')


# registration page
@app.route('/register-another-user', methods=['GET', 'POST'])
def registracija():

    if request.method == 'GET':
        data, _, _, _ = getTemperatureData(
            mysql, session)
        users = getAllUsers(mysql)
        return render_template('register_another_user.html', data=data,  users=users)
    elif request.method == 'POST':
        cursor = mysql.connection.cursor()
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        user = getUser(mysql, session)

        if user:
            # User already exists
            return render_template('register_another_user.html', error='This email is already in use')
        else:

            # Insert the new user into the database
            query = "INSERT INTO users (firstName, lastName, email, password,role) VALUES (%s, %s, %s, UNHEX(SHA2(%s, 256)),%s)"
            cursor.execute(
                query, (firstName, lastName, email, password, role,))
            mysql.connection.commit()
            cursor.close()
            data, _, _, _ = getTemperatureData(
                mysql, session)
            users = getAllUsers(mysql)
            return render_template('register_another_user.html', data=data,  users=users, user=user), 303


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index')), 303


@app.route("/send-value")
def receive_value():
    value = request.args.get("value")
    if value:
        storeTemperature(mysql, value)
        return 'Value stored'
    return 'Value not recieved'


@app.route('/update_temperature')
def update_temperature():
    temperature = getLastTempFromDB(mysql)
    return str(temperature)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
