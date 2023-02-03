def getTemperatureData(mysql, session):
    cursor = mysql.connection.cursor()
    query = f'SELECT firstName, lastName FROM users WHERE email = %s;'
    cursor.execute(query, (session['username'],))
    data = cursor.fetchone()
    query = f'SELECT date_time,value FROM temperature ORDER BY id DESC LIMIT 30;'
    cursor.execute(query)
    tempData = cursor.fetchall()
    temperatures = []
    dates = []
    query = f'SELECT value FROM temperature ORDER BY id DESC LIMIT 1;'
    cursor.execute(query)
    lastTemp = cursor.fetchone()[0]

    for temp in tempData:
        temperatures.append(temp[1])
        dates.append((temp[0].strftime("%H:%M:%S")))

    mysql.connection.commit()
    cursor.close()
    return data, temperatures, dates, lastTemp


def storeTemperature(mysql, value):
    temp = float(value)
    print('Recieved value:', temp)
    cursor = mysql.connection.cursor()
    query = "INSERT INTO temperature (date_time, value) VALUES (NOW() , %s);"
    cursor.execute(query, (temp,))

    # starting to delete data from db after there are at least 30 temperatures
    query = "SELECT * FROM temperature"
    cursor.execute(query,)
    temperatures = cursor.fetchall()
    if len(temperatures) > 30:
        query = "DELETE FROM temperature ORDER BY id ASC LIMIT 1;"
        cursor.execute(query,)

    mysql.connection.commit()
    cursor.close()


def getLastTempFromDB(mysql):
    cursor = mysql.connection.cursor()
    query = f'SELECT value FROM temperature ORDER BY id DESC LIMIT 1;'
    cursor.execute(query)
    temperature = cursor.fetchone()[0]
    mysql.connection.commit()
    cursor.close()

    return temperature


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
