#encoding: utf-8
import time
import os

def getDate(year,month,day) :
    stringMonth = str(month)
    stringDay   = str(day)

    if day < 10 :
        stringDay = "0" + stringDay
    elif day > 31 :
        day = 1
        stringDay = "01"
        month = month + 1
        stringMonth = str(month)
    if month < 10 :
        stringMonth = "0" + stringMonth
    if month > 12 :
        month = 1
        stringMonth = "01"
        year = year + 1
    stringYear  = str(year)

    formatDate = stringYear + "-" + stringMonth + "-" + stringDay
    if isDateValidate(formatDate) :
        return [stringYear + stringMonth + stringDay, formatDate, year, month, day]
    else :
        day = day + 1
        return getDate(year, month, day)

def isDateValidate(date) :
    try:
        time.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False

def readDataFromFile(type, fromDate, toDate) :
    year  = int(fromDate[0 : 4])
    month = int(fromDate[4 : 6])
    day   = int(fromDate[6 : 8])
    data  = []

    if len(fromDate) == 8 :
        if not(os.path.exists(type + "/" + fromDate) and os.path.exists(type + "/" + toDate)) :
            return data

        while True :
            currentDateGroup = getDate(year, month, day)
            currentDate = currentDateGroup[0]
            [year, month, day] = currentDateGroup[2:]

            fileName = type + "/" + currentDate
            if not os.path.exists(fileName) :
                day = day + 1
                continue
            else :
                fileObject = open(fileName)
                for line in fileObject :
                    data.append(line.strip())
                fileObject.close()
            if currentDate == toDate :
                break
            day = day + 1

        return data
    else :
        # TODO
        return data

def getTime(total, number, dataFolder) :
    intNumber = int(number)
    hour = 0
    min  = 0
    if dataFolder[0:5] == "CQSSC" :

        if total > 72 :
            if intNumber < 24 :
                [hour, min] = calculateTime(intNumber, 0, 0, 5, 0)
            else :
                if intNumber > 96 :
                    [hour, min] = calculateTime(intNumber - 96, 22, 0, 5, 0)
                else :
                    [hour, min] = calculateTime(intNumber - 23, 9, 50, 10, 0)
        else :
            [hour, min] = calculateTime(intNumber, 9, 50, 10, 0)

    elif dataFolder[0:5] == "JXSSC" :
        step = calculateStep(intNumber)
        [hour, min] = calculateTime(intNumber, 8, 59, 10, step)

    else :
        return "null"

    stringHour = str(hour)
    stringMin  = str(min)

    if hour < 10 :
        stringHour = "0" + stringHour
    if hour == 24 :
        stringHour = "00"
    if min < 10 :
        stringMin  = "0" + stringMin

    return stringHour + ":" + stringMin + ":" + "00"

def calculateStep(number) : #expected : 7767767767764
    bigStep    = 3
    big        = number / 20
    bigReserve = number % 20
    small = bigReserve / 7
    return big * bigStep + small

def calculateTime(intNumber, startHour, startMin, step, adjust) :
    totalMove = intNumber * step  + startMin + adjust
    hour = startHour + totalMove / 60
    min  = totalMove % 60
    return [hour, min]