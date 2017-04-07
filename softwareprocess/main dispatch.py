#
# from softwareprocess import dispatch as dp
#
# a = dp.calculateGHA({ 'date': '2016-01-17', 'time': '03:15:42'})
#
# print a

import xlrd
data = xlrd.open_workbook('201720Assignment5.xls')
table = data.sheet_by_name("Stars")
# starsDict = {}
# for line in table:
#     eachLine = line
#     eachLine = eachLine.split()
#     starsDict[eachLine[0]] = str(eachLine[1]) + ' ' + str(eachLine[2])
# table.close()
