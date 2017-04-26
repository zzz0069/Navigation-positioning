
from softwareprocess import dispatch as dp
a = dp.dispatch({'op':'predict', 'body': 'Betelgeuse', 'date': '2016-01-17', 'time': '03:15:42'})
print a
