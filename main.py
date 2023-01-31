from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

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
    print(session)

    if 'username' in session:

        cursor = mysql.connection.cursor()
        query = f'SELECT firstName, lastName FROM users WHERE email = %s'
        cursor.execute(query, (session['username'],))
        data = cursor.fetchone()
        data1 = cursor.fetchall()

        return render_template('index.html', data=data)

    return redirect(url_for('login')), 303


# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        cursor = mysql.connection.cursor()
        email = request.form.get('email')
        password = sha256(request.form.get('password').encode()).hexdigest()
        query = f"SELECT * FROM users WHERE HEX(password) = %s AND email = %s"
        cursor.execute(query, (password, email,))

        user = cursor.fetchone()
        mysql.connection.commit()
        cursor.close()
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


if __name__ == '__main__':
    app.run()
