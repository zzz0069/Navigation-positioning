    data = xlrd.open_workbook('201720Assignment5.xls')
    table = open(data.sheet_by_name("Stars"))
    starsDict = {}
    for line in table:
        eachLine = line
        eachLine = eachLine.split()
        starsDict[eachLine[0]] = str(eachLine[1]) + ' ' + str(eachLine[2])
        print starsDict
    table.close()
