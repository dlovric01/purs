def getTemperatureData(mysql, session):
    cursor = mysql.connection.cursor()
    query = f'SELECT firstName, lastName FROM users WHERE email = %s;'
    cursor.execute(query, (session['username'],))
    data = cursor.fetchone()
    query = f'SELECT DATE_FORMAT(date_time,"%hh:%mm"),value FROM temperature ORDER BY id DESC LIMIT 20;'
    cursor.execute(query)
    tempData = cursor.fetchall()
    temperatures = []
    dates = []
    query = f'SELECT value FROM temperature ORDER BY id DESC LIMIT 1;'
    cursor.execute(query)
    lastTemp = cursor.fetchone()[0]

    for temp in tempData:
        temperatures.append(temp[1])
        dates.append(temp[0])

    mysql.connection.commit()
    cursor.close()
    return data, temperatures, dates, lastTemp


def storeTemperature(mysql, value):
    temp = float(value)
    print('Recieved value:', temp)
    cursor = mysql.connection.cursor()
    query = "INSERT INTO temperature (date_time, value) VALUES (NOW() , %s);"
    cursor.execute(query, (temp,))
    mysql.connection.commit()
    cursor.close()
