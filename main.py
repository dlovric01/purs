from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from functions import storeTemperature, getTemperatureData, getLastTempFromDB, checkDBforUser

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
        return render_template('index.html', data=data, temperatures=temperatures, dates=dates, lastTemp=lastTemp)

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
@app.route('/register', methods=['GET', 'POST'])
def registracija():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        cursor = mysql.connection.cursor()
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user:
            # User already exists
            return render_template('register.html', error='This email is already in use')
        else:

            session['username'] = email
            # Insert the new user into the database
            query = "INSERT INTO users (firstName, lastName, email, password) VALUES (%s, %s, %s, UNHEX(SHA2(%s, 256)))"
            cursor.execute(query, (firstName, lastName, email, password,))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('index')), 303


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
