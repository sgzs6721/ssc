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
from email.mime.text import MIMEText
import smtplib

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
        time = ":".join(td[2].text.encode("utf8").split(" "))
        dataNumberDiv = td[3].div.findAll("span")
        dataNumber = ""
        for span in dataNumberDiv :
            dataNumber = dataNumber + span.text.encode("utf8")
        # print str(index) + "-" + dataNumber

        lineNumber = " ".join([date, time, dataNumber,
                              checkThree(dataNumber[0:3]),
                              checkThree(dataNumber[2:])])
        data.append(lineNumber)
    data.reverse()
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

                if continued >= continueNumber : # Continued Number
                    continueInfo = {
                        "index" :index,
                        "date" : baseDate,
                        "currentDate" : posInfo[1:],
                        "continue" : continued,
                        "group" : group,
                        "type"  : continueType
                    }
            else :
                if continued >= breakNumber : # Statistic for break and then continued number
                    breakContinuedNumber = 0
                    breakInfo = {
                        "index" : index,
                        "date" : baseDate,
                        "currentDate" : posInfo[1:],
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

        if continued > continueNumber :
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

def getMessage(info, chanel) :
    content = ""
    positionArray = ["万", "千", "百", "十", "个"]
    numberTypeEvenOdd    = ["双", "单"]

    subject = ""
    mailTepl = string.Template(
"""$currentTime
彩种: $title
模式: $mode
位置: $position位
类型: [$position]位连续[$continued]期出[$numberType]
号码: [$dateNumber - $currentNumber]
          $group
推荐: [$nextDateNumber]期起投注[$position]位[$suggestType]
===========================
"""
    )
    tepl = string.Template(
"""#####$currentTime
===========================
#### **彩种**: **$title**
#### **模式**: **$mode**
#### **位置**: **$position位**
#### **类型**: [**$position**]位连续[**$continued**]期出[**$numberType**]
#### **号码**: [$dateNumber] - [$currentNumber]
          $group
#### **推荐**: [$nextDateNumber]期起投注[**$position**]位[**$suggestType**]
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

                    markTag = "#####"
                    if chanel == "mail" : markTag = ""
                    subject = subject + markTag + title + positionArray[i.get("index")]+ \
                              numberType + mode + str(i.get("continue")) + "\n"

                    templateData = {
                        "mode" : mode,
                        "position" : positionArray[i.get("index")],
                        "continued" : i.get("continue"),
                        "numberType" : numberType,
                        "group" : numbers,
                        "suggestType" : suggestType,
                        "title" : title + "时时彩",
                        "breaked" : i.get("break"),
                        "date"    : i.get("date")[1],
                        "dateNumber" : i.get("date")[0],
                        "currentTime" : time.strftime('%Y-%m-%d %H:%M:%S'),
                        "currentNumber" : i.get("currentDate")[0],
                        "nextDateNumber" : getNextNumber(i.get("currentDate")[0], key)
                    }
                    if not chanel == "mail" :
                        content = content + tepl.substitute(templateData)
                    else :
                        content = content + mailTepl.substitute(templateData)
    print content
    return [subject, content]

def getNextNumber(date, type) :
    dateNumber = int(date[8:])
    dateTime = datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
    maxNumber = {"cq" : 120, "jx" :"084", "xj" :"96", "tj" : "084"}
    if dateNumber > int(maxNumber[type]) :
        number = 1
        dateTime = dateTime + datetime.timedelta(days=1)
    else :
        number = dateNumber + 1
    formatString =  "%0" + str(len(maxNumber[type])) + "d"
    return dateTime.strftime("%Y%m%d") + formatString % number

def sendMail(mailHost, sender, toList, sub, content, postfix, mailPass, format='plain') :
    me = sender + "<" + sender + "@" + postfix + ">"

    msg = MIMEText(content,format,'utf-8')
    msg["Accept-Language"]="zh-CN"
    msg["Accept-Charset"]="ISO-8859-1,utf-8"

    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(toList)
    try:
        s = smtplib.SMTP()
        s.connect(mailHost)
        s.login(sender, mailPass)
        s.sendmail(me, toList, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False

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
        if chanel == "mail" :
            sendMail("smtp.126.com", "sgzs6721@126.com", ["sgzs6721@qq.com", "ch880221@126.com"],
                     subject, content, "126.com", "dhysgzs*211", format='plain')
            return

        postData = urllib.urlencode(parameters)
        request = urllib2.Request(url, postData)
        urllib2.urlopen(request)

allInfo = {}
for type in ["cq", "jx", "xj", "tj"] :
    data = continuedNumber(type, 8, 7, type + "_label")
    if data :
        allInfo[type] = data

[subject, messageContent] = getMessage(allInfo, "mail")
sendMessage(subject, messageContent, "mail", "")
