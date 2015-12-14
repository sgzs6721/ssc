#encoding: utf-8
# import time
import datetime
import urllib2
import os
import string
import time
from BeautifulSoup import BeautifulSoup
from pprint import pprint

def getLatestData(type) :
    date = getDataDate()
    dataArray = []
    for i in range(0, 2) :
        url = getUrl(type, date, i)
        soup = getBeautifulSoup(url)
        if soup == "" :
            return []
        oneDayData = fetchData(soup, type, date[i])
        if not len(oneDayData) == 0 :
            for record in oneDayData :
                dataArray.append(record)
    return dataArray

def fetchData(soup, type, date) :
    data = []
    if type == "XJSSC" :
        tableTr = soup.table.findAll("tr")
        realTr = tableTr[ 3 : -2 ]
        for tr in realTr :
            realTd = tr.findAll("td")[0:3]
            if realTd[2].text.encode("utf8") == "&nbsp;" :
                print "[" + type + " " + date + "]" + "No data!"
                return []
            dataNumber = realTd[2].text.encode("utf8").replace(" ",'')
            lineNumber = " ".join([date + "-" + realTd[0].text.encode("utf8")[8:],
                                   realTd[1].text.encode("utf8"),
                                   dataNumber, checkThree(dataNumber[0:3]),
                                   checkThree(dataNumber[2:])])
            data.append(lineNumber)
    else :
        div = soup.findAll(attrs={"class":"history-tab"})
        if len(div) == 0 :
            print "[" + type + " " + date + "]" + "No data!"
            return []
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
                        # print type + " " + td[0].text + " --"
                        break

                    lineNumber = " ".join([date + "-" + td[0].text.encode("utf8"), getTime(td[0].text.encode("utf8"), type),
                                           dataNumber, frontThree, endThree])
                    data.append(lineNumber)
                else :
                    break
    return data
def checkThree(dataNumber) :
    if dataNumber[0] == dataNumber[1] :
        return "1"
    if dataNumber[0] == dataNumber[2] :
        return "1"
    if dataNumber[1] == dataNumber[2] :
        return "1"
    return "0"

def getBeautifulSoup(url) :
    try :
        req = urllib2.Request(url)
        res = urllib2.urlopen(req, timeout = 15).read()
        time.sleep(2)
    except :
        print "Error in " + url
        return ""

    soup = BeautifulSoup(res)
    return soup

def getUrl(type, date, index) :
    if type == "XJSSC" :
        return "http://www.xjflcp.com/trend/analyseSSC.do?operator=goldSscTrend&type=draw"\
               + "&drawBegin=" + date[index].replace("-","") + "&drawEnd=" + date[index + 1].replace("-","")
    elif type == "JXSSC" :
        return "http://chart.cp.360.cn/kaijiang/kaijiang?lotId=258001&spanType=2&span="\
               + date[index] + "_" + date[index]
    elif type == "CQSSC" :
        return "http://chart.cp.360.cn/kaijiang/kaijiang?lotId=255401&spanType=2&span="\
               + date[index] + "_" + date[index]
    else :
        return ""

def getTime(number, type) :
    intNumber = int(number)
    hour = 0
    min  = 0
    if type[0:5] == "CQSSC" :

        if intNumber < 24 :
            [hour, min] = calculateTime(intNumber, 0, 0, 5, 0)
        else :
            if intNumber > 96 :
                [hour, min] = calculateTime(intNumber - 96, 22, 0, 5, 0)
            else :
                [hour, min] = calculateTime(intNumber - 23, 9, 50, 10, 0)
    elif type[0:5] == "JXSSC" :
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

def getDataDate() :
    yesterday = (datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    today     = datetime.date.today().strftime("%Y-%m-%d")
    tomorrow  = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    return [yesterday, today, tomorrow]

def getSplitData(type) :
    data = getLatestData(type)

    splitData = []
    if data :
        for i in range(7) :
            splitData.append([])

        for number in data :
            info       = number.split(" ")
            date       = info[0]
            time       = info[1]
            number     = info[2]
            front3     = info[3]
            end3       = info[4]

            for i in range(5) :
                splitData[i].append(" ".join([number[i], date, time]))
            splitData[5].append(" ".join([front3, date, time]))
            splitData[6].append(" ".join([end3, date, time]))

    return splitData

def continuedNumber(type, continueNumber, breakNumber, labelDir) :

    splitData = getSplitData(type)
    allMessage = []

    if splitData :
        for index, pos in enumerate(splitData) :
            if index < 5 :
                message = calculatePos(index, pos, continueNumber, breakNumber, labelDir)
                allMessage.append(message)
            else :
                message = calculateGroup(index, pos, labelDir)
                allMessage.append(message)

    return allMessage

def calculateGroup(index, data, labelDir) :
    return []

def getBaseInfo(continuedType, number) :
    if continuedType == "even-odd" :
        return number % 2
    else :
        return number > 4

def writeLabel(index, baseDate, labelDir, group) :
    if not os.path.exists(labelDir) :
        os.makedirs(labelDir)
    fileObject = open(labelDir + "/" + baseDate[0] + "-" + str(index + 1), "w")
    fileObject.write(str(baseDate) + "=>[" + str(index + 1) + "]=>" + str(group) + "(" + str(len(group)) + ")")
    fileObject.close()

def isLabelExist(index, baseDate, labelDir):
    if os.path.exists(labelDir + "/" + baseDate[0] + "[" + str(index + 1) + "]") :
        return True
    else :
        return False

def calculatePos(index, pos, continueNumber, breakNumber, labelDir) :
    baseNumber = int(pos[0].split(" ")[0])
    baseDate   = pos[0].split(" ")[1:]
    message    = []

    for continueType in ["even-odd", "size"] :

        breakContinuedNumber = 1
        continueInfo         = {}
        breakInfo            = {}
        base = getBaseInfo(continueType, baseNumber)

        condition = ""
        continued = 1
        i = 1

        group = [baseNumber]

        while i < len(pos) :
            posInfo = pos[i].split(" ")
            breakContinuedNumber = 1
            condition = getBaseInfo(continueType, int(posInfo[0]))
            if condition == base :
                continued = continued + 1
                group.append(int(posInfo[0]))

                if continued > continueNumber : # Continued Number
                    continueInfo = {
                        "index" :index,
                        "date" : baseDate,
                        "continue" : continued,
                        "group" : group,
                        "type"  : continueType
                    }
            else :
                if continued > breakNumber : # Statistic for break and then continued number
                    breakContinuedNumber = 0
                    breakInfo = {
                        "index" : index,
                        "date" : baseDate,
                        "continue" : continued,
                        "group" : group,
                        "type"  : continueType,
                        "break" : int(posInfo[0]),
                        "breakTime" : posInfo[1:]
                    }

                continued = 1
                base = condition
                group = [int(posInfo[0])]
                baseDate   = posInfo[1:]

            i = i + 1

        if continued > 7 :
            if not isLabelExist(index, baseDate, labelDir) :
                if continueInfo :
                    message.append(continueInfo)
                    writeLabel(index, baseDate, labelDir, group)

        if breakContinuedNumber == 0 :
            if breakInfo :
                message.append(breakInfo)
                writeLabel(index, baseDate, labelDir, group)

    return message

def getMessage(info) :
    content = ""
    positionArray = ["万", "千", "百", "十", "个"]
    numberTypeEvenOdd    = ["双", "单"]

    tepl = string.Template(
"""彩种: $title
模式: $mode
位置: $position
时间: [$date]-[$breakTime]
类型: [$position]位连续[$continued]期出[$numberType]
号码: $group
推荐: 投注[$position]位[$suggestType]
======================================
""")
    for key in sorted(info.keys()) :
        title = ""
        mode  = ""
        if key == "CQSSC" :
            title = "重庆"
        elif key == "JXSSC" :
            title = "江西"
        elif key == "XJSSC" :
            title = "新疆"
        # print key
        # print info[key]
        for pos in info[key] :
            if pos :
                for i in pos :
                    numberType  = ""
                    suggestType = ""
                    numbers     = str(i.get("group"))
                    if i.get("break") :
                        mode = "N-B"
                        numbers =  numbers+ " => [" + str(i.get("break")) + "]"
                    else :
                        mode = "N"
                    if i.get("type") == "even-odd" :
                        numberType = numberTypeEvenOdd[i.get("group")[0] % 2]
                        suggestType = numberTypeEvenOdd[(i.get("group")[0] + 1) % 2]
                    else :
                        if i.get("group")[0] > 4 :
                            numberType = "大"
                            suggestType = "小"
                        else :
                            numberType = "小"
                            suggestType = "大"
                    content = content + tepl.substitute(
                        mode = mode,
                        position = positionArray[i.get("index")],
                        continued = i.get("continue"),
                        numberType = numberType,
                        group = numbers,
                        suggestType = suggestType,
                        title = title + "时时彩",
                        breaked = i.get("break"),
                        date    = i.get("date")[0] + ":" + i.get("date")[1],
                        breakTime = i.get("breakTime")[0] + ":" + i.get("breakTime")[1]
                    )
    print content

allInfo = {}
for type in ["CQSSC", "JXSSC", "XJSSC"] :
    data = continuedNumber(type, 1, 2, type + "_label")
    if data :
        allInfo[type] = data

getMessage(allInfo)
