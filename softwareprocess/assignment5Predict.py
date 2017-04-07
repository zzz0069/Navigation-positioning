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
        values = calculateAltitude(values)
        return values
    elif(values['op'] == 'predict'):
        values = calculatePredict(values)
        return values
    elif(values['op'] == 'correct'):
        return values
    elif(values['op'] == 'locate'):
        return values
    else:
        values['error'] = 'op is not a legal operation'
        return values

def calculateAltitude(values):
    key = 'observation'
    if key not in dict.keys(values):
        return {'error': 'mandatory information observation missing'}
    for key in dict.keys(values):
        if key == 'altitude':
            return {'error': 'altitude has already been in parameter'}

    keys = ['altitude']
    for key in dict.keys(values):
        keys.append(key)
    key = 'height'
    if key not in values:
        values['height'] = '0'
    key = 'temperature'
    if key not in values:
        values['temperature'] = '72'
    key = 'pressure'
    if key not in values:
        values['pressure'] = '1010'
    key = 'horizon'
    if key not in values:
        values['horizon'] = 'natural'

    value = values['observation']
    if not re.match("^\d*d\d*\.\d*$", value):
        values['error'] = 'value of observation is illegal'
        return values
    observationSet = value.split('d')
    degree = int(observationSet[0])
    minute = float(observationSet[1])
    if degree > 90 or degree < 0:
        values['error'] = 'degree of observation value is illegal'
        return values
    if minute > 60 or minute < 0:
        values['error'] = 'degree of observation value is illegal'
        return values
    try:
        if float(values['height']) < 0:
            values['error'] = 'value of height is illegal'
            return values
        if int(values['temperature']) < -20 or int(values['temperature']) > 120:
            values['error'] = 'value of temperature is illegal'
            return values
        if int(values['pressure']) < 100 or int(values['pressure']) > 1100:
            values['error'] = 'value of pressure is illegal'
            return values
        if values['horizon'] != 'natural' and values['horizon'] != 'artificial':
            values['error'] = 'value of horizon is illegal'
            return values
    except ValueError:
        values['error'] = 'cast error'
        return values


    if values['horizon'] == 'natural':
        dip = (-.97 * math.sqrt(float(values['height']))) / 60
    else:
        dip = 0
    degreeInRadians = math.radians(degree + minute / 60)
    refraction = ((-.00452 * float(values['pressure'])) / (273 + (int(values['temperature']) - 32) * 5 / 9)) / math.tan(
        degreeInRadians)
    degree = degree + minute / 60
    degree = float(degree + dip + refraction)
    altitude = degreeToString(degree)
    values['altitude'] = altitude
    for key in dict.keys(values):
        if key not in keys:
            del values[key]
    return values

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

def calculatePredict(values):
    key = 'body'
    if key not in dict.keys(values):
        values['error'] = 'mandatory information body missing'
        return values
    key = 'long'
    if key in dict.keys(values):
        values['error'] = 'input contains key long'
        return values
    key = 'lat'
    if key in dict.keys(values):
        values['error'] = 'input contains key lat'
        return values


    fileName = data = xlrd.open_workbook('demo.xls')
    stars = open(fileName)
    starsDict = {}
    for line in stars:
        eachLine = line
        eachLine = eachLine.split()
        starsDict[eachLine[0]] = str(eachLine[1]) + ' ' + str(eachLine[2])
    stars.close()
    starName = values['body']
    if starName not in starsDict: # do a star name check
        values['error'] = 'star not in catalog'
        return values

    # setting default values
    keys = ['long','lat']
    for key in dict.keys(values):
        keys.append(key)
    key = 'date'
    if key not in dict.keys(values):
        values[key] = '2001-01-01'
    else:
        flag = dateTest(values['date'])
        if flag == False:
            values['error'] = 'date value is illegal'
            return values
    key = 'time'
    if key not in dict.keys(values):
        values[key] = '00:00:00'
    else:
        flag = timeTest(values)
        if flag == False:
            values['error'] = 'time value is illegal'
            return values


    starParameters = starsDict[starName]
    starParameters = starParameters.split()
    latitude = starParameters[1]
    SHA = starParameters[0]
    timeParameters = {'date' : values['date'], 'time' : values['time']}
    earthGHA = calculateGHA(timeParameters)
    long = degreeToFloat(earthGHA) + degreeToFloat(SHA)
    long = long - (int(long / 360) * 360)
    long = degreeToString(long)
    values['long'] = long
    values['lat'] = latitude
    for key in dict.keys(values):
        if key not in keys:
            del values[key]
    return values

def timeTest(values):
    # validate time
    time = values['time']
    if not re.match("^\d\d:\d\d:\d\d", time):
        return False
    time = time.split(':')
    if (int(time[0]) > 24 or int(time[0]) < 0) or (int(time[1]) > 60 or int(time[1]) < 0) or (int(time[2]) > 60 or int(time[2]) <0):
        return False


def dateTest(value):
    # validate date
    if not re.match("^\d\d\d\d-\d\d-\d\d$", value):
        return False
    value = value.split('-')
    if int(value[0]) < 2001 or int(value[1]) > 12:
        return False
    date = int(value[2])
    month = int(value[1])
    year = int(value[0])
    if month == 2 and year % 4 != 0:
        if date > 28:
            return False
    if month == 2 and year % 4 == 0:
        if date > 29:
            return False
    if month in [1, 3, 5, 7, 8, 10, 12]:
        if date > 31:
            return False
    if month in [4, 6, 9, 11]:
        if date > 30:
            return False


#calculate the GHA to the date
def calculateGHA(timeParameters):
    originalGHA = '100d42.6'
    originalGHA = degreeToFloat(originalGHA)
    date = timeParameters['date']
    time = timeParameters['time']
    year = int(date.split('-')[0])
    month = int(date.split('-')[1])
    day = int(date.split('-')[2])
    yearGap = year - 2001
    cumulativeProgress = yearGap * degreeToFloat('-0d14.31667')
    leapYears = int(yearGap / 4)
    dailyRotation = degreeToFloat('0d59.0')
    totalProgression = dailyRotation * leapYears
    # the rotation to the time
    beginningOfTheYear = datetime.date(year,1,1)
    currentDate = datetime.date(year,month,day)
    diff = currentDate - beginningOfTheYear
    dayGap = int(diff.days)
    time = time.split(':')
    sec = dayGap * 86400 + int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])
    rotationInYear = (sec - int(sec / 86164.1) * 86164.1) / 86164.1 * degreeToFloat('360d0')
    GHA = originalGHA + cumulativeProgress + totalProgression + rotationInYear
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
