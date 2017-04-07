
from softwareprocess import dispatch as dp
c=dp.degreeToFloat('0d59.0')
c *= 3
d=dp.degreeToString(c)
print d
a = dp.dispatch({'op':'predict', 'body': 'Betelgeuse', 'date': '2016-01-17', 'time': '03:15:42'})
print a
