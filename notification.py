#encoding: utf-8
# import time
import datetime
import urllib2
from BeautifulSoup import BeautifulSoup
from pprint import pprint

def getLatestData(type) :
    date = getDataDate()
    dataArray = []
    for i in range(0, 2) :
        url = getUrl(type, date, i)
        soup = getBeautifulSoup(url)
        oneDayData = fetchData(soup, type)
        if not len(oneDayData) == 0 :
            for record in oneDayData :
                dataArray.append(record)
        else :
            return []
    return dataArray

def fetchData(soup, type) :
    data = []
    if type == "XJSSC" :
        tableTr = soup.table.findAll("tr")
        realTr = tableTr[ 3 : -2 ]
        for tr in realTr :
            realTd = tr.findAll("td")[0:3]
            if realTd[2].text.encode("utf8") == "&nbsp;" :
                print "No data!"
                return []
            dataNumber = realTd[2].text.encode("utf8").replace(" ",'')
            lineNumber = " ".join([realTd[0].text.encode("utf8"),
                                   realTd[1].text.encode("utf8"),
                                   dataNumber, checkThree(dataNumber[0:3]),
                                   checkThree(dataNumber[2:])])
            data.append(lineNumber)
    else :
        print "cq and jx to be continued!"


def checkThree(dataNumber) :
    if dataNumber[0] == dataNumber[1] :
        return "1"
    if dataNumber[0] == dataNumber[2] :
        return "1"
    if dataNumber[1] == dataNumber[2] :
        return "1"
    return "0"

def getBeautifulSoup(url) :
    req = urllib2.Request(url)
    res =urllib2.urlopen(req).read()
    soup = BeautifulSoup(res)
    return soup

def getUrl(type, date, index) :
    if type == "XJSSC" :
        return "http://www.xjflcp.com/trend/analyseSSC.do?operator=goldSscTrend&type=draw"\
               + "&drawBegin=" + date[index] + "&drawEnd=" + date[index + 1]
    elif type == "JXSSC" :
        return "http://chart.cp.360.cn/kaijiang/kaijiang?lotId=258001&spanType=2&span="\
               + date[index + 1] + "_" + date[index + 1]
    elif type == "CQSSC" :
        return "http://chart.cp.360.cn/kaijiang/kaijiang?lotId=255401&spanType=2&span="\
               + date[index + 1] + "_" + date[index + 1]
    else :
        return ""


def getDataDate() :
    yesterday = (datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y%m%d")
    today     = datetime.date.today().strftime("%Y%m%d")
    tomorrow  = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y%m%d")
    return [yesterday, today, tomorrow]

getLatestData("JXSSC")
# if continued >= breakNumber : # for notification
#
#     allMessage.append(getMessage(type, index, continued, continueType, baseDate, group))
