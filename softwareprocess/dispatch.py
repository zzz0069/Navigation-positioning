import math
import re
import datetime
import xlrd

def dispatch(values=None):

    if(values == None):
        return {'error': 'parameter is missing'}
    if(not(isinstance(values,dict))):
        return {'error': 'parameter is not a dictionary'}
    if (not('op' in values)):
        values['error'] = 'no op is specified'
        return values

    if(values['op'] == 'adjust'):
        return adjust(values)
    elif(values['op'] == 'predict'):
        return predict(values)
    elif(values['op'] == 'correct'):
        return correct(values)
    elif(values['op'] == 'locate'):
        return locate(values)
    else:
        values['error'] = 'op is not a legal operation'
        return values

def adjust(values):

    if 'altitude' in values:
        values['error'] = 'altitude has already exists'
        return values

    if 'observation' not in values:
        values['error'] = 'mandatory information is missing'
        return values
    try:
        degreesMinutes = values['observation'].split('d')
        degrees = int(degreesMinutes[0])
        minutesStringType = degreesMinutes[1]
        minutes = float(minutesStringType)
    except:
        values['error'] = 'observation is invalid'
        return values
    if degrees < 0 or degrees >= 90:
        values['error'] = 'observation is invalid'
        return values
    if minutesStringType[::-1].find('.') is not 1:
        values['error'] = 'observation is invalid'
        return values
    if minutes < 0.0 or minutes >= 60.0:
        values['error'] = 'observation is invalid'
        return values
    if degrees == 0 and minutes == 0.1:
        values['error'] = 'observation is invalid'
        return values
    observation = degrees + minutes / 60.0
 #   print observation
    height = 0
    if 'height' in values:
        try:
            height = float(values['height'])
        except ValueError:
            values['error'] = 'height is invalid'
            return values
        if values['height'] < 0:
            values['error'] = 'height is invalid'
            return values
 #   print height
    temperature = 72
    if 'temperature' in values:
        try:
            temperature = int(values['temperature'])
        except ValueError:
            values['error'] = 'temperature is invalid'
            return values
        if temperature < -20 or temperature > 120:
            values['error'] = 'temperature is invalid'
            return values
 #   print temperature
    pressure = 1010
    if 'pressure' in values:
        try:
            pressure = int(values['pressure'])
        except ValueError:
            values['error'] = 'pressure is invalid'
            return values
        if pressure < 100 or pressure > 1100:
            values['error'] = 'pressure is invalid'
            return values
  #  print pressure
    horizon = 'natural'
    if 'horizon' in values:
        horizon = values['horizon']
        if horizon != 'artificial' and horizon != 'natural':
            values['error'] = 'horizon is invalid'
            return values
#    print horizon
    dip = 0
    if horizon == 'natural':
        dip = (-0.97 * math.sqrt(height)) / 60
#  print dip
    refraction=(-0.00452*pressure) / (273+convertToCelsius(temperature))/math.tan(math.radians(observation))
#    print refraction
    altitude = observation + dip + refraction
    if altitude < 0 or altitude > 90:
        values['error'] = 'altitude is invalid'
        return values
    values['altitude'] = correctedAltitude(altitude)
    return values

def correctedAltitude(alt):
    x = ((alt - math.floor(alt)) * 60.0)
    arcmin = round(x,1)
    return str(int(math.floor(alt))) + 'd' + str(arcmin)

def convertToCelsius(f):
    c = (f - 32) * 5.0/9.0
    return c

def predict(values):
    key = 'body'
    if key not in dict.keys(values):
        values['error'] = 'mandatory information is missing'
        return values
    key = 'lat'
    if key in dict.keys(values):
        values['error'] = 'input contains key : lat'
        return values
    key = 'long'
    if key in dict.keys(values):
        values['error'] = 'input contains key : long'
        return values


    data = xlrd.open_workbook('C:\Users\yymjz\PycharmProjects\CSSE\softwareprocess\ 201720Assignment5.xls')
    table = data.sheet_by_name("Stars")
    starsDict = {}
    for line in table:
        eachLine = line
        eachLine = eachLine.split()
        starsDict[eachLine[0]] = str(eachLine[1]) + ' ' + str(eachLine[2])
    table.close()
    starName = values['body']
    if starName not in starsDict:
        values['error'] = 'star not in catalog'
        return values

    keys = ['long','lat']
    for key in dict.keys(values):
        keys.append(key)
    key = 'date'
    if key not in dict.keys(values):
        values[key] = '2001-01-01'
    else:
        dateValid = dateTest(values['date'])
        if dateValid == False:
            values['error'] = 'invalid date'
            return values
    key = 'time'
    if key not in dict.keys(values):
        values[key] = '00:00:00'
    else:
        timeValid = timeTest(values)
        if timeValid == False:
            values['error'] = 'invalid time'
            return values


    starParameters = starsDict[starName]
    starParameters = starParameters.split()
    SHA = starParameters[0]
    latitude = starParameters[1]
    timeParameters = {'date' : values['date'], 'time' : values['time']}
    GHAEarth = calculateGHA(timeParameters)
    GHAStar = degreeToFloat(GHAEarth) + degreeToFloat(SHA)
    print GHAStar
    GHAStar = GHAStar - (int(GHAStar / 360) * 360)
    print GHAStar
    GHAStar = degreeToString(GHAStar)
    values['long'] = GHAStar
    values['lat'] = latitude
    for key in dict.keys(values):
        if key not in keys:
            del values[key]
    return values

def dateTest(value):
    if not re.match("^\d\d\d\d-\d\d-\d\d$", value):
        return False
    value = value.split('-')
    if int(value[0]) < 2001 or int(value[1]) < 1 or int(value[1]) > 12:
        return False
    year = int(value[0])
    month = int(value[1])
    date = int(value[2])

    if month in [1, 3, 5, 7, 8, 10, 12]:
        if date > 31:
            return False
    if month in [4, 6, 9, 11]:
        if date > 30:
            return False
    if month == 2 and year % 4 != 0:
        if date > 28:
            return False
    if month == 2 and year % 4 == 0:
        if date > 29:
            return False

def timeTest(values):
    time = values['time']
    if not re.match("^\d\d:\d\d:\d\d", time):
        return False
    time = time.split(':')
    if (int(time[0]) > 24 or int(time[0]) < 0) or (int(time[1]) > 60 or int(time[1]) < 0) or (int(time[2]) > 60 or int(time[2]) <0):
        return False

def calculateGHA(timeParameters):
    originalGHA = '100d42.6'        # GHA in 2001-01-01
    originalGHA = degreeToFloat(originalGHA)
    date = timeParameters['date']
    time = timeParameters['time']
    year = int(date.split('-')[0])
    month = int(date.split('-')[1])
    day = int(date.split('-')[2])
    yearGap = year - 2001
    cumulativeProgression = yearGap * degreeToFloat('-0d14.31667')
    leapYears = int(yearGap / 4)
    dailyRotation = degreeToFloat('0d59.0')
    totalProgression = dailyRotation * leapYears
    firstDayOfTheYear = datetime.date(year,1,1)
    currentDate = datetime.date(year,month,day)
    dayDiff = currentDate - firstDayOfTheYear
    dayGap = int(dayDiff.days)
    time = time.split(':')
    secGap = dayGap * 86400 + int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])
    rotationInYear = (secGap - int(secGap / 86164.1) * 86164.1) / 86164.1 * degreeToFloat('360d00.0')
    GHA = originalGHA + cumulativeProgression + totalProgression + rotationInYear
    GHA = degreeToString(GHA)
    return GHA

def degreeToFloat(degree):
    degree = degree.split('d')
    minute = float(degree[1])
    if int(degree[0]) != 0:
        if degree[0] < 0:
            degree = int(degree[0]) - minute / 60
        else:
            degree = int(degree[0]) + minute / 60
    else:
        if degree[0][0] == '-':
            degree = - minute / 60
        else:
            degree = minute / 60
    return degree

def degreeToString(degree):
    minute = str("{:.1f}".format((degree - int(degree)) * 60))
    if '-' in minute:
        minute = minute.replace('-', '')
    minute = minute.split('.')
    var1 = minute[0].zfill(2)
    var2 = minute[1]
    minute = var1 + '.' + var2
    degree = str(int(degree)) + 'd' + minute
    return degree

def correct(values):
    return values

def locate(values):
    return values
