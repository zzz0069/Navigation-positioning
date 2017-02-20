
import urllib
import re

def convertString2Dictionary(inputString=''):

    errorDict = {'error':'true'}

    url = urllib.unquote(inputString)
    splitStr = re.split(",|=", url)
    keyValueList = []
    for str1 in splitStr:
        keyValueList.append(str1.lstrip().rstrip())

    if len(keyValueList) == 1:
        return errorDict

    key = [0] * ((len(splitStr) + 1) / 2)
    value = [0] * ((len(splitStr) + 1) / 2)

    for i in range(0, len(keyValueList)):
        if i % 2 == 0:
            if keyValueList[i] in key:
                return errorDict
            else:
                key[i / 2] = keyValueList[i]
        else:
            value[i / 2] = keyValueList[i]

    for i in key:
        if not validKey(i):
            return errorDict

    for i in value:
        if not validValue(i):
            return errorDict

    outputDict = dict(zip(key, value))

    return outputDict

def validKey(input_string=""):

    return input_string.isalnum() and input_string[:1].isalpha()

def validValue(input_string=""):

    return input_string.isalnum()




