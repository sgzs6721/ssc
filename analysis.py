#encoding: utf-8
# import time
import datetime
import urllib
import urllib2
import os
import string
import time
from BeautifulSoup import BeautifulSoup
from pprint import pprint

def getLatestData(type) :
    dataArray = []

    url = getUrl(type)
    soup = getBeautifulSoup(url)
    if soup == "" :
        return []
    oneDayData = fetchData(soup, type)
    if not len(oneDayData) == 0 :
        for record in oneDayData :
            dataArray.append(record)
    return dataArray

def fetchData(soup, type) :
    data = []
    tableTr = soup.findAll("table")[1].findAll("tr")[1:]

    for index, tr in enumerate(tableTr) :
        td = tr.findAll("td")
        date = td[1].span.text.encode("utf8")
        time = td[2].text.encode("utf8")[11:]
        dataNumberDiv = td[3].div.findAll("span")
        dataNumber = ""
        for span in dataNumberDiv :
            dataNumber = dataNumber + span.text.encode("utf8")
        # print str(index) + "-" + dataNumber

        lineNumber = " ".join([date, time, dataNumber,
                              checkThree(dataNumber[0:3]),
                              checkThree(dataNumber[2:])])
        data.append(lineNumber)
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
    except :
        print "Error in " + url
        return ""

    soup = BeautifulSoup(res)
    return soup

def getUrl(type) :
    return "http://www.caipiaow.com/index.php?m=kaijiang&a=index&cz=" + type + "&type=ssc"

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

def writeLabel(index, baseDate, labelDir, group, br) :
    if not os.path.exists(labelDir) :
        os.makedirs(labelDir)
    fileObject = open(labelDir + "/" + baseDate[0] + "-" + str(index + 1) + br, "w")
    fileObject.write(str(baseDate) + "=>[" + str(index + 1) + "]=>" + str(group) + "(" + str(len(group)) + br + ")")
    fileObject.close()

def isLabelExist(index, baseDate, labelDir, br):
    if os.path.exists(labelDir + "/" + baseDate[0] + "-" + str(index + 1) + br) :
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
            if not isLabelExist(index, baseDate, labelDir, "") :
                if continueInfo :
                    message.append(continueInfo)
            writeLabel(index, baseDate, labelDir, group, "")

        if breakContinuedNumber == 0 :
            if not isLabelExist(index, baseDate, labelDir, "B") :
                if breakInfo :
                    message.append(breakInfo)
            writeLabel(index, baseDate, labelDir, group, "B")

    return message

def getMessage(info) :
    content = ""
    positionArray = ["万", "千", "百", "十", "个"]
    numberTypeEvenOdd    = ["双", "单"]

    subject = ""
    tepl = string.Template(
"""#####$currentTime
===========================
#### **彩种**: **$title**
#### **模式**: **$mode**
#### **位置**: **$position位**
#### **时间**: [$date]
#### **类型**: [**$position**]位连续[**$continued**]期出[**$numberType**]
#### **号码**: $group
#### **推荐**: 投注[**$position**]位[**$suggestType**]
""")
    for key in sorted(info.keys()) :
        title = ""
        mode  = ""
        if key == "cq" :
            title = "重庆"
        elif key == "jx" :
            title = "江西"
        elif key == "xj" :
            title = "新疆"
        elif key == "tj" :
            title = "天津"
        print key
        print info[key]
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

                    subject = subject + "#####" + title + positionArray[i.get("index")]+ \
                              numberType + mode + str(i.get("continue")) + "\n"

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
                        currentTime = time.strftime('%Y-%m-%d %H:%M:%S')
                    )
    print content
    return [subject, content]

def sendMessage(subject, content, chanel, mobile) :
    if content :
        content = subject + content
        subject = "时时彩计划方案"
        if chanel == "serverChan" :
            key = "SCU749Tfa80c68db4805b9421f52d360f6614cb565696559f19e"
            url = "http://sc.ftqq.com/" + key +".send"
            parameters = {
            "text" : subject, "desp" : content,
            "key"  : key
            }
        elif chanel == "pushBear" :
            url = "http://api.pushbear.com/smart"
            parameters = {
                "sendkey" : "96-d296f0cdb565bae82a833fabcd860309",
                "text" : subject,
                "mobile" : mobile,
                "desp" : content
            }

        postData = urllib.urlencode(parameters)
        request = urllib2.Request(url, postData)
        urllib2.urlopen(request)

allInfo = {}
for type in ["cq", "jx", "xj", "tj"] :
# for type in ["CQSSC", "XJSSC"] :
    data = continuedNumber(type, 8, 6, type + "_label")
    if data :
        allInfo[type] = data

[subject, messageContent] = getMessage(allInfo)
sendMessage(subject, messageContent, "serverChan", "")
