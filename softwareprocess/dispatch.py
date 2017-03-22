import math

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
        return {'error':'mandatory information is missing'}
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
    return values

def correct(values):
    return values

def locate(values):
    return values
