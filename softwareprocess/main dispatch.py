#
# from softwareprocess import dispatch as dp
#
# a = dp.calculateGHA({ 'date': '2016-01-17', 'time': '03:15:42'})
#
# print a
data = open('Stars.txt','r')
starsDict = {}
for line in data.readline():
    print line
    # eachLine = line
    # eachLine = eachLine.split()
    # starsDict[eachLine[0]] = str(eachLine[1]) + ' ' + str(eachLine[2])
data.close()
# starsDict = {}
# for line in table:
#     eachLine = line
#     eachLine = eachLine.split()
#     starsDict[eachLine[0]] = str(eachLine[1]) + ' ' + str(eachLine[2])
# table.close()
