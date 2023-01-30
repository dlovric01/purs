from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from hashlib import sha256

app = Flask(__name__)
# define secret key for session
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

# mysql database parameters
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'app'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'baza'

# access database
mysql = MySQL(app)


# starting page with temperature data
@app.route('/', methods=['GET'])
def pocetna():
    print(session)

    if 'username' in session:
        return render_template('index.html')

    return redirect(url_for('login')), 303


# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = sha256(request.form.get('password').encode()).hexdigest()
        cursor = mysql.connection.cursor()
        query = f"SELECT * FROM users WHERE HEX(password) = '{password}' AND email = '{email}'"
        cursor.execute(query)

        user = cursor.fetchone()
        if user:
            # user is valid to login
            session['username'] = email
            return redirect(url_for('pocetna')), 303
        else:
            return render_template('login.html', error='Incorrect email or password')


# registration page
@app.route('/register', methods=['GET', 'POST'])
def registracija():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        # firstName = request.form.get('firstName')
        # lastName = request.form.get('lastName')
        # email = request.form.get('email')
        # password = request.form.get('password')

        # if email == 'test@gmail.com' and password == 'test':
        #     session['username'] = 'test'
        #     return redirect(url_for('pocetna')), 303
        # else:
        #     return render_template('login.html', error='Uneseni su krivi korisnički podaci')
        return ''


if __name__ == '__main__':
    app.run()
