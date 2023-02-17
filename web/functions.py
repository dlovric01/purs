

def getTemperatureData(mysql, table):
    cursor = mysql.connection.cursor()
    query = f'SELECT date_time,value FROM {table} ORDER BY id DESC LIMIT 30;'
    cursor.execute(query)
    tempData = cursor.fetchall()
    temperatures = []
    dates = []
    for temp in tempData:
        temperatures.append(temp[1])
        dates.append((temp[0].strftime("%H:%M:%S")))

    mysql.connection.commit()
    cursor.close()
    return temperatures, dates


def storeTemperature(mysql, value, table):
    temp = float(value)
    cursor = mysql.connection.cursor()
    query = f"INSERT INTO {table} (date_time, value) VALUES (NOW() , %s);"
    cursor.execute(query, (temp,))

    query = f"SELECT * FROM {table}"
    cursor.execute(query,)
    temperatures = cursor.fetchall()
    # starting to delete data from db after there are at least 30 temperatures
    if len(temperatures) > 30:
        query = f"DELETE FROM {table} ORDER BY id ASC LIMIT 1;"
        cursor.execute(query,)

    mysql.connection.commit()
    cursor.close()


def getCurrentTemperature(mysql, dt, table):
    cursor = mysql.connection.cursor()
    query = f'SELECT value,date_time FROM {table} ORDER BY id DESC LIMIT 1;'
    cursor.execute(query)
    try:
        response = cursor.fetchone()
        temperature = response[0]
        lastDateFromDB = response[1]
        dateNow = dt.datetime.now()

        # compares date and if there are 10 seconds appart it means sensor is not working
        isSensorConnected = compare_dates(lastDateFromDB, dateNow)

        mysql.connection.commit()
        cursor.close()

        return temperature, isSensorConnected
    except:
        return 0, False,


def checkDBforUser(mysql, request, sha256):
    cursor = mysql.connection.cursor()
    email = request.form.get('email')
    password = sha256(request.form.get('password').encode()).hexdigest()
    query = f"SELECT * FROM users WHERE HEX(password) = %s AND email = %s"
    cursor.execute(query, (password, email,))
    user = cursor.fetchone()
    mysql.connection.commit()
    cursor.close()

    return user, email


def getAllUsers(mysql):
    cursor = mysql.connection.cursor()
    query = f'SELECT firstName,lastName,email,role FROM users;'
    cursor.execute(query)
    data = cursor.fetchall()
    users = []
    for row in data:
        users.append({
            'firstName': row[0],
            'lastName': row[1],
            'email': row[2],
            'role': row[3]
        })

    mysql.connection.commit()
    cursor.close()

    return users


def getUser(mysql, session):
    cursor = mysql.connection.cursor()
    query = f'SELECT firstName,lastName,email,role FROM users WHERE email = %s;'
    cursor.execute(query, ({session["username"]},))
    response = cursor.fetchone()
    user = ({
        'firstName': response[0],
        'lastName': response[1],
        'email': response[2],
        'role': response[3],
    })

    return user


def getTargetedTemperature(mysql):
    cursor = mysql.connection.cursor()
    query = f'SELECT value FROM targetedTemperature;'
    cursor.execute(query, )
    temp = cursor.fetchone()[0]
    mysql.connection.commit()
    cursor.close()
    return temp


def storeTargetedTemperature(mysql, request):
    cursor = mysql.connection.cursor()
    query = f"REPLACE INTO targetedTemperature (id,value) VALUES (1,%s);"
    cursor.execute(query, (request.form.get('value'),))
    mysql.connection.commit()
    cursor.close()


def storeDevicesStatus(mysql, request):
    cursor = mysql.connection.cursor()
    fan = request.args.get('fan')
    radiator = request.args.get('radiator')
    query = f"REPLACE INTO devicesStatus (id,fan,radiator,date_time) VALUES (1,%s,%s,NOW());"
    cursor.execute(query, (fan, radiator,))
    mysql.connection.commit()
    cursor.close()


def getDevicesStatus(mysql, dt):
    cursor = mysql.connection.cursor()
    query = f'SELECT * FROM devicesStatus;'
    cursor.execute(query, )
    devices = cursor.fetchone()
    dateNow = dt.datetime.now()
    devicesStatus = ({
        'fan': devices[1],
        'radiator': devices[2],
    })
    areDevicesConnected = compare_dates(devices[3], dateNow)
    mysql.connection.commit()
    cursor.close()
    return devicesStatus, areDevicesConnected


def checkIfEmailExists(mysql, request):
    cursor = mysql.connection.cursor()
    email = request.form.get('email')
    query = f'SELECT email FROM users WHERE email = %s;'
    cursor.execute(query, (email,))
    email = cursor.fetchone()
    mysql.connection.commit()
    cursor.close()
    return email


def registerUser(mysql, request):
    cursor = mysql.connection.cursor()
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')
    query = "INSERT INTO users (firstName, lastName, email, password,role) VALUES (%s, %s, %s, UNHEX(SHA2(%s, 256)),%s)"
    cursor.execute(
        query, (firstName, lastName, email, password, role,))
    mysql.connection.commit()
    cursor.close()


def compare_dates(date1, date2):
    if date2 > date1:
        difference = date2 - date1
        if difference.total_seconds() < 10:
            return True
    return False
