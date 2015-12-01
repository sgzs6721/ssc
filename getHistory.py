#encoding: utf-8
import urllib
import urllib2
import xml.dom.minidom

from pprint import pprint
import time
import os
from BeautifulSoup import BeautifulSoup

def getBeautifulSoup(url) :
    req = urllib2.Request(url)
    res =urllib2.urlopen(req).read()
    soup = BeautifulSoup(res)
    return soup

def writeDataToFileJx(soup, fileName, dir) :
    div = soup.find(attrs={'class','bonusNum_box newNum'})
    print div

def writeDataToFileXJ(soup, fileName, dir) :
    tableTr = soup.table.findAll("tr")
    realTr = tableTr[ 3 : -2 ]
    if not os.path.exists(dir) :
        os.makedirs(dir)

    writeTag = False
    for tr in realTr :
        realTd = tr.findAll("td")[0:3]
        if not writeTag :
            if realTd[2].text.encode("utf8") == "&nbsp;" :
                print  fileName + ", no data!"
                return
            else :
                writeTag = True
                dataObject = open(dir + "/" + fileName, "w+")
        dataNumber = realTd[2].text.encode("utf8").replace(" ",'')

        lineNumber = " ".join([realTd[0].text.encode("utf8"),
                               realTd[1].text.encode("utf8"),
                               dataNumber, checkThree(dataNumber[0:3]),
                               checkThree(dataNumber[2:])])
        dataObject.write(lineNumber)
        dataObject.write("\n")

    dataObject.close()
    print "Create File " + fileName

def checkThree(dataNumber) :
    if dataNumber[0] == dataNumber[1] :
        return "1"
    if dataNumber[0] == dataNumber[2] :
        return "1"
    if dataNumber[1] == dataNumber[2] :
        return "1"
    return "0"

def getDate(year,month,day) :
    stringYear  = year
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

    if isDateValidate(str(stringYear) + "-" + stringMonth + "-" + stringDay) :
        return [str(stringYear) + stringMonth + stringDay, year, month, day]
    else :
        day = day + 1
        return getDate(stringYear, month, day)

def getFormatDate(year, month, day) :
    stringYear  = str(year)
    stringMonth = str(month)
    stringDay   = str(day)
    if day < 10 :
        stringDay = "0" + stringDay
    if month < 10 :
        stringMonth = "0" + stringMonth

    return stringYear + "-" + stringMonth + "-" + stringDay

def isDateValidate(date) :
    try:
        time.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False

dateYear  = 2015
dateMonth = 11
dateDay   = 28

dataFolder = "XJSSC"

def getHistoryXJ(dateYear, dateMonth, dateDay, dataFolder) :
    currentDate = getDate(dateYear, dateMonth, dateMonth)
    fromDate = currentDate[0]
    [dateYear, dateMonth, dateDay] = currentDate[1:]
    endDate = getDate(dateYear, dateMonth, dateDay + 1)[0]

    if os.path.exists(dataFolder + "/" + fromDate) :
        print "skip " + fromDate
        return
    else :
        url = "http://www.xjflcp.com/trend/analyseSSC.do?operator=goldSscTrend&type=draw&drawBegin="\
         + fromDate + "&drawEnd=" + endDate
        s = getBeautifulSoup(url)
        writeDataToFileXJ(s, fromDate, dataFolder)

while True :
    currentDate = getDate(dateYear, dateMonth, dateDay)
    fromDate = currentDate[0]
    [dateYear, dateMonth, dateDay] = currentDate[1:]

    if dateYear == time.localtime()[0] and dateMonth == time.localtime()[1] and dateDay == time.localtime()[2] :
        break

    if os.path.exists(dataFolder + "/" + fromDate) :
        dateDay = dateDay + 1
        print "skip " + fromDate
        continue
    endDate = getDate(dateYear, dateMonth, dateDay + 1)[0]

    xj = "http://www.xjflcp.com/trend/analyseSSC.do?operator=goldSscTrend&type=draw&drawBegin="\
         + fromDate + "&drawEnd=" + endDate #20070812
    s = getBeautifulSoup(xj)
    writeDataToFileXJ(s, fromDate, dataFolder)
    dateDay = dateDay + 1

