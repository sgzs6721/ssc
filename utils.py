#encoding: utf-8
import time

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