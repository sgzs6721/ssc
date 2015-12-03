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

def writeDataToFile(soup, fileName, dir) :
    div = soup.findAll(attrs={"class":"history-tab"})
    if len(div) == 0 :
        print  fileName + ", no data!"
        return
    dataObject = open(dir + "/" + fileName, "w+")
    for i in range(1,4) :
        column = div[0].findAll(attrs={"class":"tr-odd" + str(i)})[0].tbody.findAll("tr")
        for index in column :
            td = index.findAll("td")
            if not td[0].text == '' :
                dataNumber = td[1].text.encode("utf8")
                frontThree = 0
                endThree   = 0
                if not (dataNumber == "" or dataNumber == '- -'):
                    frontThree = checkThree(dataNumber[0:3])
                    endThree   = checkThree(dataNumber[2:])
                else :
                    continue
                lineNumber = " ".join([fileName+td[0].text.encode("utf8"), "time",
                                       dataNumber, frontThree, endThree])
                dataObject.write(lineNumber)
                dataObject.write("\n")

            else :
                break
    dataObject.close()
    print "Create File " + fileName

def writeDataToFileXJ(soup, fileName, dir) :
    tableTr = soup.table.findAll("tr")
    realTr = tableTr[ 3 : -2 ]

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

    formatDate = str(stringYear) + "-" + stringMonth + "-" + stringDay
    if isDateValidate(formatDate) :
        return [str(stringYear) + stringMonth + stringDay, formatDate, year, month, day]
    else :
        day = day + 1
        return getDate(stringYear, month, day)

def isDateValidate(date) :
    try:
        time.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False

def getHistoryXJ(dateYear, dateMonth, dateDay, dataFolder) :
    currentDate = getDate(dateYear, dateMonth, dateDay)
    fromDate = currentDate[0]
    [dateYear, dateMonth, dateDay] = currentDate[2:]
    endDate = getDate(dateYear, dateMonth, dateDay + 1)[0]

    if not os.path.exists(dataFolder) :
        os.makedirs(dataFolder)

    if os.path.exists(dataFolder + "/" + fromDate) :
        print "skip " + fromDate
    else :
        url = "http://www.xjflcp.com/trend/analyseSSC.do?operator=goldSscTrend&type=draw&drawBegin="\
         + fromDate + "&drawEnd=" + endDate
        s = getBeautifulSoup(url)
        writeDataToFileXJ(s, fromDate, dataFolder)

    return [dateYear, dateMonth, dateDay]

def getHistory(dateYear, dateMonth, dateDay, dataFolder, lotId) :
    currentDate = getDate(dateYear, dateMonth, dateDay)
    fromDate = currentDate[1]
    [dateYear, dateMonth, dateDay] = currentDate[2:]

    if os.path.exists(dataFolder + "/" + fromDate) :
        print "skip " + fromDate

    url = "http://chart.cp.360.cn/kaijiang/kaijiang?lotId="+lotId+"&spanType=2&span="+fromDate+"_" + fromDate
    s = getBeautifulSoup(url)
    if not os.path.exists(dataFolder) :
        os.makedirs(dataFolder)
    writeDataToFile(s, currentDate[0], dataFolder)
    return [dateYear, dateMonth, dateDay]

def getAllHistoryXJ(year, month, day, dataFolder) :
    while True :
        if year == time.localtime()[0] and month == time.localtime()[1] and day == time.localtime()[2] :
            break
        [year, month, day] = getHistoryXJ(year, month, day, dataFolder)
        day = day + 1

def getAllHistory(year, month, day, dataFolder, lotId) :
    while True :
        if year == time.localtime()[0] and month == time.localtime()[1] and day == time.localtime()[2] :
            break
        [year, month, day] = getHistory(year, month, day, dataFolder, lotId)
        day = day + 1

getAllHistoryXJ(2007, 8, 12, "XJSSC")
getAllHistory(2009, 8, 24, "JXSSC", "258001")
getAllHistory(2009, 12, 13, "CQSSC", "255401")
