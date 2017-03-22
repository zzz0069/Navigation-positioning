import math

def dispatch(values=None):

    if(values == None):
        return {'error': 'parameter is missing'}
    if(not(isinstance(values,dict))):
        return {'error': 'parameter is not a dictionary'}
    if (not('op' in values)):
        return {'error': 'no op is specified'}

    if(values['op'] == 'adjust'):
        return adjust(values)
    elif(values['op'] == 'predict'):
        return values
    elif(values['op'] == 'correct'):
        return values
    elif(values['op'] == 'locate'):
        return values
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
        degreesAndMinutes = values['observation'].split('d')
        degrees = int(degreesAndMinutes[0])
        minutesStr = degreesAndMinutes[1]
        minutes = float(minutesStr)
    except:
        values['error'] = 'observation is invalid'
        return values
    if degrees < 0 or degrees >= 90:
        values['error'] = 'observation is invalid'
        return values
    if minutesStr[::-1].find('.') is not 1:
        # minutes must be a float with a mandatory decimal [0.0, 60.0)
        values['error'] = 'observation is invalid'
        return values
    if minutes < 0.0 or minutes >= 60.0:
        values['error'] = 'observation is invalid'
        return values
    if degrees == 0 and minutes == 0.1:
        values['error'] = 'observation is invalid'
        return values
    totalDegrees = degrees + minutes / 60.0

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

    horizon = 'natural'
    if 'horizon' in values:
        if horizon != 'artificial' and horizon != 'natural':
            values['error'] = 'horizon is invalid'
            return values

    dip = 0
    if horizon == 'natural':
        dip = (-0.97 * math.sqrt(height)) / 60.0
    refraction=(-0.00452*pressure) / (273+convertToCelsius(temperature))/math.tan(totalDegrees)
    altitude = totalDegrees + dip + refraction
    if altitude < 0 or altitude > 90:
        values['error'] = 'altitude is invalid'
        return values
    #values['altitude'] = altitude
    values['altitude'] = formatAlt(altitude)
    return values

def formatAlt(alt):
    x = ((alt - math.floor(alt)) * 60.0)
    arcmin = round(x,1)
    return arcmin
    #return '%dd%.1f' % (math.floor(alt), arcmin)

def convertToCelsius(f):
    c = (f - 32) * 5.0/9.0
    return c

def transToDegrees(min):
    return min / 60.0

def predict(values):
    return values

def correct(values):
    return values

def locate(values):
    return values
