#encoding: utf-8
import urllib2
import utils

import time
import os
import codecs
from BeautifulSoup import BeautifulSoup

def getBeautifulSoup(url) :
    req = urllib2.Request(url)
    res =urllib2.urlopen(req).read()
    soup = BeautifulSoup(res)
    return soup

def writeDataToFile(soup, fileName, dir) :
    if os.path.exists(dir + "/" + fileName) :
        print "Skip " + dir + "/" + fileName
        return
    else :
        div = soup.findAll(attrs={"class":"history-tab"})
        if len(div) == 0 :
            print  fileName + ", no data!"
            return
        dataObject = open(dir + "/" + fileName, "w")
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
                    lineNumber = " ".join([fileName+td[0].text.encode("utf8"), utils.getTime(120, td[0].text.encode("utf8"), dir),
                                           dataNumber, frontThree, endThree])
                    dataObject.write(lineNumber)
                    dataObject.write("\n")

                else :
                    break
        dataObject.close()
        print "Create File " + dir + "/" + fileName

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
    print "Create File " + dir + "/" +fileName

def checkThree(dataNumber) :
    if dataNumber[0] == dataNumber[1] :
        return "1"
    if dataNumber[0] == dataNumber[2] :
        return "1"
    if dataNumber[1] == dataNumber[2] :
        return "1"
    return "0"

def isDateValidate(date) :
    try:
        time.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False

def getHistoryXJ(dateYear, dateMonth, dateDay, dataFolder) :
    currentDate = utils.getDate(dateYear, dateMonth, dateDay)
    fromDate = currentDate[0]
    [dateYear, dateMonth, dateDay] = currentDate[2:]
    endDate = utils.getDate(dateYear, dateMonth, dateDay + 1)[0]

    if not os.path.exists(dataFolder) :
        os.makedirs(dataFolder)

    if os.path.exists(dataFolder + "/" + fromDate) :
        print "skip " + dataFolder + "/" +  fromDate
    else :
        url = "http://www.xjflcp.com/trend/analyseSSC.do?operator=goldSscTrend&type=draw&drawBegin="\
         + fromDate + "&drawEnd=" + endDate
        s = getBeautifulSoup(url)
        writeDataToFileXJ(s, fromDate, dataFolder)

    return [dateYear, dateMonth, dateDay]

def getHistory(dateYear, dateMonth, dateDay, dataFolder, lotId) :
    currentDate = utils.getDate(dateYear, dateMonth, dateDay)
    fromDate = currentDate[1]
    [dateYear, dateMonth, dateDay] = currentDate[2:]

    if os.path.exists(dataFolder + "/" + fromDate) :
        print "skip " + dataFolder + "/" + fromDate

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

def generateHistory(dataFolder, inputFile) :
    fileObject = codecs.open(inputFile, "r", "utf_8_sig")
    datetime = ""
    outputObject = ""
    dayArray = []
    for line in fileObject :
        date = line.split("-")[0]
        if not date == datetime :
            if not len(dayArray) == 0 :
                dayArray.reverse()
                writeArrayToFile(dayArray, datetime, dataFolder)
                dayArray = []
        dayArray.append(line.strip())
        datetime = date
    if not len(dayArray) == 0 :
        writeArrayToFile(dayArray, datetime, dataFolder)

def writeArrayToFile(array, date, dataFolder) :
    if not os.path.exists(dataFolder) :
        os.makedirs(dataFolder)

    if os.path.exists(dataFolder + "/" + date) :
        print "skip " + dataFolder + "/" + date
    else :
        outputObject = open(dataFolder + "/" + date, "w+")
        totalNumber = len(array)
        for line in array :
            info = line.split("\t")
            dateNumber = info[0].split("-")[1]
            dataNumber = info[1]
            frontThree = checkThree(dataNumber[0:3])
            endThree   = checkThree(dataNumber[2:])
            time = utils.getTime(totalNumber, dateNumber, dataFolder)
            newLine = " ".join([date + dateNumber, time,
                                dataNumber, frontThree, endThree])
            outputObject.write(newLine)
            outputObject.write("\n")
        outputObject.close()
        print "Create File " + dataFolder + "/" + date

# get data from file to file(formated like XJ)
# generateHistory("CQSSC", "cqssc.txt") # end 20151202
# generateHistory("JXSSC", "jxssc.txt") # end 20151202
getAllHistoryXJ(2015, 8, 12, "XJSSC") # end current date

# get from 360
# getAllHistory(2015, 12, 1, "JXSSC_360", "258001")
# getAllHistory(2009, 12, 13, "CQSSC_360", "255401")
